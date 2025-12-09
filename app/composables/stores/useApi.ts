import type { Note } from '../../../model/Note'
import type { ActionItem } from '../../../model/ActionItem'

// API response types that match backend snake_case format
interface ApiNote {
	id: string
	title: string
	attendees?: string[]
	meeting_start_time?: string
	content: string
	created_at: string
	updated_at?: string
	action_items: ApiActionItem[]
}

interface ApiActionItem {
	id: string
	title: string
	note_id?: string
	created_at: string
	updated_at?: string
	completed_at?: string
	completed: boolean
}

// Transform API response to frontend model
function transformNote(apiNote: ApiNote): Note {
	return {
		id: apiNote.id,
		title: apiNote.title,
		attendees: apiNote.attendees,
		meetingStartTime: apiNote.meeting_start_time ? new Date(apiNote.meeting_start_time) : undefined,
		content: apiNote.content,
		createdAt: new Date(apiNote.created_at),
		updatedAt: apiNote.updated_at ? new Date(apiNote.updated_at) : undefined,
		actionItems: apiNote.action_items.map(transformActionItem)
	}
}

function transformActionItem(apiItem: ApiActionItem): ActionItem {
	return {
		id: apiItem.id,
		title: apiItem.title,
		noteId: apiItem.note_id,
		createdAt: apiItem.created_at ? new Date(apiItem.created_at) : undefined,
		updatedAt: apiItem.updated_at ? new Date(apiItem.updated_at) : undefined,
		completedAt: apiItem.completed_at ? new Date(apiItem.completed_at) : null,
		completed: apiItem.completed
	}
}

// Base API client for backend communication
export const useApi = () => {
	// API base URL - FastAPI backend
	const baseURL = 'http://localhost:8000/api'

	const apiClient = $fetch.create({
		baseURL,
		headers: {
			'Content-Type': 'application/json'
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
		// Transform to API format (snake_case)
		const apiPayload = {
			title: noteData.title || '',
			attendees: noteData.attendees,
			meeting_start_time: noteData.meetingStartTime?.toISOString(),
			content: noteData.content || '',
			action_items: noteData.actionItems?.map(ai => ({ title: ai.title }))
		}

		const response = await apiClient<ApiNote>('/notes', {
			method: 'POST',
			body: apiPayload
		})

		return transformNote(response)
	}

	const updateNote = async (id: string, noteData: Partial<Note>): Promise<Note> => {
		// Transform to API format (snake_case)
		const apiPayload: Record<string, unknown> = {}

		if (noteData.title !== undefined) apiPayload.title = noteData.title
		if (noteData.attendees !== undefined) apiPayload.attendees = noteData.attendees
		if (noteData.meetingStartTime !== undefined) apiPayload.meeting_start_time = new Date(noteData.meetingStartTime)?.toISOString()
		if (noteData.content !== undefined) apiPayload.content = noteData.content
		if (noteData.actionItems !== undefined) apiPayload.action_items = noteData.actionItems.map(ai => ({ title: ai.title }))

		const response = await apiClient<ApiNote>(`/notes/${id}`, {
			method: 'PUT',
			body: apiPayload
		})

		return transformNote(response)
	}

	const getNote = async (id: string): Promise<Note> => {
		const response = await apiClient<ApiNote>(`/notes/${id}`)
		return transformNote(response)
	}

	const getNotes = async (date?: string): Promise<Note[]> => {
		const query = date ? `?date=${date}` : ''
		const response = await apiClient<ApiNote[]>(`/notes${query}`)
		return response.map(transformNote)
	}

	const getTodaysNotes = async (): Promise<Note[]> => {
		const response = await apiClient<ApiNote[]>('/notes/today')
		return response.map(transformNote)
	}

	const getYesterdaysNotes = async (): Promise<Note[]> => {
		const response = await apiClient<ApiNote[]>('/notes/yesterday')
		return response.map(transformNote)
	}

	const deleteNote = async (id: string): Promise<void> => {
		await apiClient(`/notes/${id}`, {
			method: 'DELETE'
		})
	}

	return {
		createNote,
		updateNote,
		getNote,
		getNotes,
		getTodaysNotes,
		getYesterdaysNotes,
		deleteNote
	}
}

// Action Items API endpoints
export const useActionItemsApi = () => {
	const { apiClient } = useApi()

	const createActionItem = async (itemData: Partial<ActionItem>): Promise<ActionItem> => {
		const apiPayload = {
			title: itemData.title || '',
			note_id: itemData.noteId
		}

		const response = await apiClient<ApiActionItem>('/action-items', {
			method: 'POST',
			body: apiPayload
		})

		return transformActionItem(response)
	}

	const getActionItem = async (id: string): Promise<ActionItem> => {
		const response = await apiClient<ApiActionItem>(`/action-items/${id}`)
		return transformActionItem(response)
	}

	const getActionItems = async (params?: { noteId?: string; incompleteOnly?: boolean; limit?: number }): Promise<ActionItem[]> => {
		const queryParams = new URLSearchParams()
		if (params?.noteId) queryParams.append('note_id', params.noteId)
		if (params?.incompleteOnly) queryParams.append('incomplete_only', 'true')
		if (params?.limit) queryParams.append('limit', params.limit.toString())

		const query = queryParams.toString() ? `?${queryParams.toString()}` : ''
		const response = await apiClient<ApiActionItem[]>(`/action-items${query}`)
		return response.map(transformActionItem)
	}

	const getIncompleteActionItems = async (limit = 5): Promise<ActionItem[]> => {
		const response = await apiClient<ApiActionItem[]>(`/action-items/incomplete?limit=${limit}`)
		return response.map(transformActionItem)
	}

	const updateActionItem = async (id: string, itemData: Partial<ActionItem>): Promise<ActionItem> => {
		const apiPayload: Record<string, unknown> = {}

		if (itemData.title !== undefined) apiPayload.title = itemData.title
		if (itemData.completed !== undefined) apiPayload.completed = itemData.completed

		const response = await apiClient<ApiActionItem>(`/action-items/${id}`, {
			method: 'PUT',
			body: apiPayload
		})

		return transformActionItem(response)
	}

	const completeActionItem = async (id: string): Promise<ActionItem> => {
		const response = await apiClient<ApiActionItem>(`/action-items/${id}/complete`, {
			method: 'POST'
		})
		return transformActionItem(response)
	}

	const uncompleteActionItem = async (id: string): Promise<ActionItem> => {
		const response = await apiClient<ApiActionItem>(`/action-items/${id}/uncomplete`, {
			method: 'POST'
		})
		return transformActionItem(response)
	}

	const deleteActionItem = async (id: string): Promise<void> => {
		await apiClient(`/action-items/${id}`, {
			method: 'DELETE'
		})
	}

	return {
		createActionItem,
		getActionItem,
		getActionItems,
		getIncompleteActionItems,
		updateActionItem,
		completeActionItem,
		uncompleteActionItem,
		deleteActionItem
	}
}
