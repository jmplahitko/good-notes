import type { Note } from '../../../model/Note';
import { useNotesApi } from './useApi';

// Reactive state (module-level for singleton behavior)
const notes = ref<Note[]>([])
const currentNote = ref<Note | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Notes store composable
export const useNotesStore = () => {
	// API client
	const {
		createNote: apiCreateNote,
		updateNote: apiUpdateNote,
		getNote: apiGetNote,
		getNotes: apiGetNotes,
		deleteNote: apiDeleteNote
	} = useNotesApi()

	// Actions
	const search = async (query?: string): Promise<Note[]> => {
		loading.value = true
		error.value = null

		try {
			// TODO: Pass query to backend when Elasticsearch is ready
			const fetchedNotes = await apiGetNotes()
			notes.value = fetchedNotes
			return fetchedNotes
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to fetch notes'
			throw err
		} finally {
			loading.value = false
		}
	}

	const create = async (noteData: Partial<Note>): Promise<Note> => {
		loading.value = true
		error.value = null

		try {
			const createdNote = await apiCreateNote(noteData)
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
			const updatedNote = await apiUpdateNote(id, noteData)
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
			const note = await apiGetNote(id)
			currentNote.value = note
			return note
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to fetch note'
			throw err
		} finally {
			loading.value = false
		}
	}

	const del = async (id: string): Promise<void> => {
		loading.value = true
		error.value = null

		try {
			await apiDeleteNote(id)
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
		search,
		create,
		update,
		get,
		del,
		clearError
	}
}
