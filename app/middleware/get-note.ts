import { useNotesStore } from '../composables/stores/useNotesStore'

export default defineNuxtRouteMiddleware(async (to) => {
	// Get note ID from route params
	const noteId = to.params.id as string

	if (!noteId) {
		throw createError({
			statusCode: 404,
			statusMessage: 'Note ID is required'
		})
	}

	try {
		// Fetch note data using the store
		const notesStore = useNotesStore()
		await notesStore.fetchNoteById(noteId)

		// Note data is now available in the store's reactive state
		// Page component can access it via notesStore.currentNote
	} catch (error) {
		throw createError({
			statusCode: 404,
			statusMessage: 'Note not found'
		})
	}
})
