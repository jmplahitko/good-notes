import type { ActionItem } from '../../../model/ActionItem';
import { useActionItemsApi } from './useApi';

// Reactive state (module-level for singleton behavior)
const actionItems = ref<ActionItem[]>([])
const currentActionItem = ref<ActionItem | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Action items store composable
export const useActionItemsStore = () => {
	// API client
	const {
		createActionItem: apiCreateActionItem,
		getActionItems: apiGetActionItems,
		getActionItem: apiGetActionItem,
		updateActionItem: apiUpdateActionItem,
		completeActionItem: apiCompleteActionItem,
		uncompleteActionItem: apiUncompleteActionItem,
		deleteActionItem: apiDeleteActionItem
	} = useActionItemsApi()

	// Actions
	const fetch = async (params?: { noteId?: string; incompleteOnly?: boolean; limit?: number }): Promise<ActionItem[]> => {
		loading.value = true
		error.value = null

		try {
			const fetchedActionItems = await apiGetActionItems(params)
			actionItems.value = fetchedActionItems
			return fetchedActionItems
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to fetch action items'
			throw err
		} finally {
			loading.value = false
		}
	}

	const create = async (actionItemData: Partial<ActionItem>): Promise<ActionItem> => {
		loading.value = true
		error.value = null

		try {
			const createdActionItem = await apiCreateActionItem(actionItemData)
			actionItems.value = [createdActionItem, ...actionItems.value]
			currentActionItem.value = createdActionItem
			return createdActionItem
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to create action item'
			throw err
		} finally {
			loading.value = false
		}
	}

	const update = async (id: string, actionItemData: Partial<ActionItem>): Promise<ActionItem> => {
		loading.value = true
		error.value = null

		try {
			const updatedActionItem = await apiUpdateActionItem(id, actionItemData)
			actionItems.value = actionItems.value.map(ai => ai.id === id ? updatedActionItem : ai)
			if (currentActionItem.value?.id === id) {
				currentActionItem.value = updatedActionItem
			}
			return updatedActionItem
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to update action item'
			throw err
		} finally {
			loading.value = false
		}
	}

	const get = async (id: string): Promise<ActionItem> => {
		loading.value = true
		error.value = null

		try {
			const actionItem = await apiGetActionItem(id)
			currentActionItem.value = actionItem
			return actionItem
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to fetch action item'
			throw err
		} finally {
			loading.value = false
		}
	}

	const toggleCompletion = async (id: string): Promise<ActionItem> => {
		loading.value = true
		error.value = null

		try {
			const actionItem = actionItems.value.find(ai => ai.id === id)
			if (!actionItem) {
				throw new Error('Action item not found')
			}

			let updatedActionItem: ActionItem
			if (actionItem.completed) {
				updatedActionItem = await apiUncompleteActionItem(id)
			} else {
				updatedActionItem = await apiCompleteActionItem(id)
			}

			actionItems.value = actionItems.value.map(ai => ai.id === id ? updatedActionItem : ai)
			if (currentActionItem.value?.id === id) {
				currentActionItem.value = updatedActionItem
			}
			return updatedActionItem
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to toggle action item completion'
			throw err
		} finally {
			loading.value = false
		}
	}

	const del = async (id: string): Promise<void> => {
		loading.value = true
		error.value = null

		try {
			await apiDeleteActionItem(id)
			actionItems.value = actionItems.value.filter(ai => ai.id !== id)
			if (currentActionItem.value?.id === id) {
				currentActionItem.value = null
			}
		} catch (err) {
			error.value = err instanceof Error ? err.message : 'Failed to delete action item'
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
		actionItems: readonly(actionItems),
		currentActionItem: readonly(currentActionItem),
		loading: readonly(loading),
		error: readonly(error),

		// Actions
		fetch,
		create,
		update,
		get,
		toggleCompletion,
		del,
		clearError
	}
}
