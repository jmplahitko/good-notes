import type { ActionItem } from '../../model/ActionItem'

// Mock action items store
const mockActionItems = ref<ActionItem[]>([
	{
		id: 'action-1',
		title: 'Fix mobile responsiveness issues',
		completed: false,
		noteId: 'note-1',
		createdAt: new Date('2024-11-15T10:00:00'),
		updatedAt: new Date('2024-11-15T10:00:00'),
		completedAt: null
	},
	{
		id: 'action-2',
		title: 'Update API documentation',
		completed: true,
		noteId: 'note-1',
		createdAt: new Date('2024-11-10T14:30:00'),
		updatedAt: new Date('2024-11-12T16:00:00'),
		completedAt: new Date('2024-11-12T16:00:00')
	},
	{
		id: 'action-3',
		title: 'Review and merge pull requests',
		completed: false,
		noteId: 'note-3',
		createdAt: new Date('2024-11-08T11:15:00'),
		updatedAt: new Date('2024-11-08T11:15:00'),
		completedAt: null
	},
	{
		id: 'action-4',
		title: 'Create presentation slides for Q4 review',
		completed: true,
		noteId: 'note-2',
		createdAt: new Date('2024-10-25T09:45:00'),
		updatedAt: new Date('2024-10-28T13:20:00'),
		completedAt: new Date('2024-10-28T13:20:00')
	},
	{
		id: 'action-5',
		title: 'Gather Q4 metrics and KPIs',
		completed: true,
		noteId: 'note-2',
		createdAt: new Date('2024-10-20T16:00:00'),
		updatedAt: new Date('2024-10-22T10:30:00'),
		completedAt: new Date('2024-10-22T10:30:00')
	},
	{
		id: 'action-6',
		title: 'Schedule follow-up meeting with client',
		completed: false,
		noteId: 'note-2',
		createdAt: new Date('2024-10-18T08:30:00'),
		updatedAt: new Date('2024-10-18T08:30:00'),
		completedAt: null
	},
	{
		id: 'action-7',
		title: 'Implement security fixes',
		completed: true,
		noteId: 'note-3',
		createdAt: new Date('2024-10-15T12:00:00'),
		updatedAt: new Date('2024-10-17T14:45:00'),
		completedAt: new Date('2024-10-17T14:45:00')
	},
	{
		id: 'action-8',
		title: 'Add performance optimizations',
		completed: false,
		noteId: 'note-3',
		createdAt: new Date('2024-10-12T15:30:00'),
		updatedAt: new Date('2024-10-12T15:30:00'),
		completedAt: null
	}
])

export function useActionItems() {
	// Add new action item
	const addActionItem = (itemData: Omit<ActionItem, 'id' | 'createdAt' | 'updatedAt'>) => {
		const newItem: ActionItem = {
			...itemData,
			id: `action-${Date.now()}`,
			createdAt: new Date(),
			updatedAt: new Date()
		}
		mockActionItems.value.unshift(newItem)
		console.log('Created new action item:', newItem.id)
		return newItem
	}

	// Update existing action item
	const updateActionItem = (id: string, updates: Partial<ActionItem>) => {
		const itemIndex = mockActionItems.value.findIndex((item: ActionItem) => item.id === id)
		if (itemIndex !== -1) {
			mockActionItems.value[itemIndex] = {
				...mockActionItems.value[itemIndex],
				...updates,
				updatedAt: new Date()
			}
			console.log('Updated action item:', id)
			return mockActionItems.value[itemIndex]
		}
		return null
	}

	// Delete action item
	const deleteActionItem = (id: string) => {
		const itemIndex = mockActionItems.value.findIndex(item => item.id === id)
		if (itemIndex !== -1) {
			mockActionItems.value.splice(itemIndex, 1)
			console.log('Deleted action item:', id)
			return true
		}
		return false
	}

	// Toggle completion
	const toggleCompletion = (id: string) => {
		const item = mockActionItems.value.find(item => item.id === id)
		if (item) {
			const wasCompleted = item.completed
			item.completed = !wasCompleted
			item.completedAt = item.completed ? new Date() : null
			item.updatedAt = new Date()
			console.log('Toggled completion for:', id)
			return item
		}
		return null
	}

	return {
		actionItems: readonly(mockActionItems),
		addActionItem,
		updateActionItem,
		deleteActionItem,
		toggleCompletion
	}
}
