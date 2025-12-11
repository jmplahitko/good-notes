<template>
	<UContainer class="py-6">
		<div class="max-w-6xl mx-auto">
			<!-- Search and Filters -->
			<div class="mb-6">
				<div class="flex gap-4 mb-4">
					<UInput v-model="searchQuery" variant="subtle" size="lg" placeholder="Search action items..." icon="i-heroicons-magnifying-glass" class="flex-1 max-w-md" />
					<USelectMenu v-model="statusFilter" :options="statusOptions" placeholder="Filter by status" class="w-48" />
					<USelectMenu v-model="sortBy" :options="sortOptions" placeholder="Sort by" class="w-48" />
				</div>

				<!-- Results count -->
				<p class="text-sm text-muted">
					{{ filteredActionItems.length }} action item{{ filteredActionItems.length !== 1 ? 's' : '' }}
					{{ searchQuery ? `for "${searchQuery}"` : '' }}
				</p>
			</div>

			<!-- Action Items List -->
			<div class="space-y-4">
				<div v-for="item in filteredActionItems" :key="item.id" class="bg-elevated/15 rounded-lg p-6 hover:bg-elevated/25 transition-colors">
					<div class="flex items-start justify-between">
						<div class="flex items-start gap-4 flex-1">
							<!-- Completion Checkbox -->
							<UCheckbox :model-value="item.completed" @update:model-value="toggleCompletionLocal(item)" class="mt-1" />

							<div class="flex-1">
								<!-- Title -->
								<h3 class="text-lg font-medium mb-2" :class="{ 'line-through text-muted': item.completed }">
									{{ item.title }}
								</h3>

								<!-- Metadata -->
								<div class="flex flex-wrap items-center gap-4 text-sm text-muted">
									<div class="flex items-center gap-1">
										<UIcon name="i-heroicons-calendar" class="h-4 w-4" />
										<span>Created: {{ formatDate(item.createdAt) }}</span>
									</div>
									<div v-if="item.completedAt" class="flex items-center gap-1">
										<UIcon name="i-heroicons-check-circle" class="h-4 w-4 text-success" />
										<span>Completed: {{ formatDate(item.completedAt) }}</span>
									</div>
									<div v-if="item.noteId" class="flex items-center gap-1">
										<UIcon name="i-heroicons-document-text" class="h-4 w-4" />
										<span>Note: {{ item.noteId }}</span>
									</div>
								</div>
							</div>
						</div>

						<!-- Actions -->
						<div class="flex items-center gap-2 ml-4">
							<UButton variant="ghost" size="sm" icon="i-heroicons-pencil-square" @click="editActionItem(item)">
								Edit
							</UButton>
							<UButton variant="ghost" size="sm" icon="i-heroicons-trash" color="error" @click="deleteActionItem(item)">
								Delete
							</UButton>
						</div>
					</div>
				</div>
			</div>

			<!-- Empty State -->
			<div v-if="filteredActionItems.length === 0" class="text-center py-12">
				<UIcon name="i-heroicons-clipboard-document-list" class="mx-auto h-16 w-16 text-muted opacity-50 mb-4" />
				<h3 class="text-xl font-medium mb-2">No action items found</h3>
				<p class="text-muted mb-4">
					{{ searchQuery ? 'Try adjusting your search or filters.' : 'Create your first action item to get started.' }}
				</p>
			</div>
		</div>
	</UContainer>
</template>

<script setup lang="ts">
import type { ActionItem } from '../../../model/ActionItem'
import { useActionItems } from '../../composables/useActionItems'

// Use the shared action items composable
const { actionItems, addActionItem, updateActionItem, deleteActionItem: _deleteActionItem, toggleCompletion } = useActionItems()

// Reactive state
const searchQuery = ref('')
const statusFilter = ref('all')
const sortBy = ref('created-desc')
const showCreateModal = ref(false)
const editingItem = ref<ActionItem | null>(null)

// Form data for create/edit
const formData = ref({
	title: '',
	noteId: '',
	completed: false
})

// Filter options
const statusOptions = [
	{ label: 'All', value: 'all' },
	{ label: 'Completed', value: 'completed' },
	{ label: 'Incomplete', value: 'incomplete' }
]

const sortOptions = [
	{ label: 'Created (Newest First)', value: 'created-desc' },
	{ label: 'Created (Oldest First)', value: 'created-asc' },
	{ label: 'Title (A-Z)', value: 'title-asc' },
	{ label: 'Title (Z-A)', value: 'title-desc' },
	{ label: 'Completed (Newest First)', value: 'completed-desc' },
	{ label: 'Completed (Oldest First)', value: 'completed-asc' }
]

// Filtered and sorted action items
const filteredActionItems = computed(() => {
	let items = [...actionItems.value]

	// Apply search filter
	if (searchQuery.value.trim()) {
		const query = searchQuery.value.toLowerCase()
		items = items.filter(item =>
			item.title.toLowerCase().includes(query) ||
			item.noteId?.toLowerCase().includes(query)
		)
	}

	// Apply status filter
	if (statusFilter.value !== 'all') {
		items = items.filter(item =>
			statusFilter.value === 'completed' ? item.completed : !item.completed
		)
	}

	// Apply sorting
	items.sort((a, b) => {
		switch (sortBy.value) {
			case 'created-desc':
				return new Date(b.createdAt || 0).getTime() - new Date(a.createdAt || 0).getTime()
			case 'created-asc':
				return new Date(a.createdAt || 0).getTime() - new Date(b.createdAt || 0).getTime()
			case 'title-asc':
				return a.title.localeCompare(b.title)
			case 'title-desc':
				return b.title.localeCompare(a.title)
			case 'completed-desc':
				return new Date(b.completedAt || 0).getTime() - new Date(a.completedAt || 0).getTime()
			case 'completed-asc':
				return new Date(a.completedAt || 0).getTime() - new Date(b.completedAt || 0).getTime()
			default:
				return 0
		}
	})

	return items
})

// Toggle completion status
const toggleCompletionLocal = (item: ActionItem) => {
	toggleCompletion(item.id)
}

// Edit action item
const editActionItem = (item: ActionItem) => {
	editingItem.value = item
	formData.value = {
		title: item.title,
		noteId: item.noteId || '',
		completed: item.completed || false
	}
	showCreateModal.value = true
}

// Delete action item
const deleteActionItem = (item: ActionItem) => {
	// In a real app, this would show a confirmation dialog
	if (confirm(`Delete action item "${item.title}"?`)) {
		const index = mockActionItems.indexOf(item)
		if (index > -1) {
			mockActionItems.splice(index, 1)
		}
		// In a real app, this would call an API
		console.log('Deleted action item:', item.id)
	}
}

// Save action item (create or update)
const saveActionItem = () => {
	if (!formData.value.title.trim()) return

	if (editingItem.value) {
		// Update existing item
		updateActionItem(editingItem.value.id, {
			title: formData.value.title,
			noteId: formData.value.noteId || undefined,
			completed: formData.value.completed,
			completedAt: formData.value.completed ? new Date() : null
		})
	} else {
		// Create new item
		addActionItem({
			title: formData.value.title,
			noteId: formData.value.noteId || undefined,
			completed: formData.value.completed,
			completedAt: formData.value.completed ? new Date() : null
		})
	}

	cancelEdit()
}

// Cancel edit/create
const cancelEdit = () => {
	showCreateModal.value = false
	editingItem.value = null
	formData.value = {
		title: '',
		noteId: '',
		completed: false
	}
}

// Format date for display
const formatDate = (date?: Date) => {
	if (!date) return 'Unknown'
	return new Intl.DateTimeFormat('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: '2-digit'
	}).format(new Date(date))
}
</script>
