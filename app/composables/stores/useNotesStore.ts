import type { Note } from '../../../model/Note';
import { useNotesApi } from './useApi';

// Notes store composable
export const useNotesStore = () => {
	// Reactive state
	const notes = ref<Note[]>([])
	const currentNote = ref<Note | null>(null)
	const loading = ref(false)
	const error = ref<string | null>(null)

	// API client
	const {
		createNote: apiCreateNote,
		getNote: apiGetNote
	} = useNotesApi()

	// Actions
	const create = async (noteData: Partial<Note>): Promise<Note> => {
		loading.value = true
		error.value = null

		try {
			// Call backend API
			const createdNote = await apiCreateNote(noteData)

			// Update store with backend response (reactive state)
			notes.value = [...notes.value, createdNote]
			currentNote.value = createdNote

			return createdNote
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to create note'
			throw err
		} finally {
			loading.value = false
		}
	}

	const update = async (id: string, noteData: Partial<Note>): Promise<Note> => {
		loading.value = true
		error.value = null

		try {
			// TODO: Call backend API when implemented
			// const updatedNote = await apiUpdateNote(id, noteData)

			// For now, update local state
			const existingNote = notes.value.find(n => n.id === id)
			if (!existingNote) {
				throw new Error('Note not found')
			}

			const updatedNote: Note = {
				...existingNote,
				...noteData,
				updatedAt: new Date()
			}

			// Update store with backend response (reactive state)
			notes.value = notes.value.map(n => n.id === id ? updatedNote : n)
			if (currentNote.value?.id === id) {
				currentNote.value = updatedNote
			}

			return updatedNote
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to update note'
			throw err
		} finally {
			loading.value = false
		}
	}

	const get = async (id: string): Promise<Note> => {
		loading.value = true
		error.value = null

		try {
			// TODO: Call backend API when implemented
			const note = await apiGetNote(id)

			if (!note) {
				throw new Error('Note not found')
			}

			currentNote.value = note
			return note
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to fetch note'
			throw err
		} finally {
			loading.value = false
		}
	}

	const search = async (): Promise<Note[]> => {
		loading.value = true
		error.value = null

		try {
			// TODO: Call backend API when implemented
			// const fetchedNotes = await apiGetNotes()

			// For now, return local state
			return notes.value
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to fetch notes'
			throw err
		} finally {
			loading.value = false
		}
	}

	const del = async (id: string): Promise<void> => {
		loading.value = true
		error.value = null

		try {
			// TODO: Call backend API when implemented
			// await apiDeleteNote(id)

			// Update local state
			notes.value = notes.value.filter(n => n.id !== id)
			if (currentNote.value?.id === id) {
				currentNote.value = null
			}
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to delete note'
			throw err
		} finally {
			loading.value = false
		}
	}

	// Clear error state
	const clearError = () => {
		error.value = null
	}

	return {
		// State
		notes: readonly(notes),
		currentNote: readonly(currentNote),
		loading: readonly(loading),
		error: readonly(error),

		// Actions
		create,
		update,
		get,
		search,
		del,
		clearError
	}
}
