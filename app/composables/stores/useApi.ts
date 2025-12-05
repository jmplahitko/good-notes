import type { Note } from '../../../model/Note';

// Base API client for backend communication
export const useApi = () => {
	const config = useRuntimeConfig()

	// API base URL - will be configured for the backend when it's implemented
	const baseURL = 'http://localhost:8000/api' // FastAPI backend

	const apiClient = $fetch.create({
		baseURL,
		headers: {
			'Content-Type': 'application/json',
		},
		onRequest({ request, options }) {
			// Add auth headers here when implemented
			console.log('API Request:', request, options)
		},
		onResponse({ response }) {
			console.log('API Response:', response)
		},
		onResponseError({ response }) {
			console.error('API Error:', response)
			throw new Error(`API Error: ${response.status} - ${response.statusText}`)
		}
	})

	return {
		apiClient
	}
}

// Note API endpoints
export const useNotesApi = () => {
	const { apiClient } = useApi()

	const createNote = async (noteData: Partial<Note>): Promise<Note> => {
		// TODO: Implement when backend is ready
		// For now, simulate API call and return mock data
		console.log('Creating note:', noteData)

		// Simulate API delay
		await new Promise(resolve => setTimeout(resolve, 500))

		// Mock response with generated ID and timestamps
		const createdNote: Note = {
			id: `note-${Date.now()}`,
			title: noteData.title || '',
			attendees: noteData.attendees || [],
			meetingStartTime: noteData.meetingStartTime,
			content: noteData.content || '',
			createdAt: new Date(),
			updatedAt: new Date(),
			actionItems: noteData.actionItems || []
		}

		return createdNote
	}

	const updateNote = async (id: string, noteData: Partial<Note>): Promise<Note> => {
		// TODO: Implement when backend is ready
		console.log('Updating note:', id, noteData)
		throw new Error('Not implemented yet')
	}

	const getNote = async (id: string): Promise<Note> => {
		// TODO: Implement when backend is ready
		console.log('Getting note:', id)
		throw new Error('Not implemented yet')
	}

	const getNotes = async (): Promise<Note[]> => {
		// TODO: Implement when backend is ready
		console.log('Getting all notes')
		return []
	}

	const deleteNote = async (id: string): Promise<void> => {
		// TODO: Implement when backend is ready
		console.log('Deleting note:', id)
		throw new Error('Not implemented yet')
	}

	return {
		createNote,
		updateNote,
		getNote,
		getNotes,
		deleteNote
	}
}
