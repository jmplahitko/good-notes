<template>
	<UContainer>
		<div class="space-y-6">

			<!-- Search Section -->
			<div class="max-w-2xl mx-auto">
				<UInput v-model="searchQuery" variant="subtle" size="lg" label="Search Notes" placeholder="Search by title, content, or attendees..." icon="i-heroicons-magnifying-glass" />
			</div>

			<!-- Results Section -->
			<div class="space-y-4">
				<div class="flex items-center justify-between">
					<h2 class="text-lg font-semibold">
						{{ searchQuery ? `${filteredNotes.length} result${filteredNotes.length !== 1 ? 's' : ''} for "${searchQuery}"` : 'All Notes' }}
					</h2>
					<UButton to="/notes/create" icon="i-heroicons-plus">
						New Note
					</UButton>
				</div>

				<!-- Loading State -->
				<div v-if="notesStore.loading.value" class="text-center py-12">
					<UIcon name="i-heroicons-arrow-path" class="mx-auto h-8 w-8 animate-spin text-primary" />
					<p class="mt-2 text-muted">Loading notes...</p>
				</div>

				<!-- Error State -->
				<div v-else-if="notesStore.error.value" class="text-center py-12">
					<UIcon name="i-heroicons-exclamation-triangle" class="mx-auto h-16 w-16 text-error mb-4" />
					<h3 class="text-xl font-medium mb-2">Failed to load notes</h3>
					<p class="text-muted mb-4">{{ notesStore.error.value }}</p>
					<UButton @click="loadNotes" icon="i-heroicons-arrow-path">
						Retry
					</UButton>
				</div>

				<!-- Search Results (Google-style) -->
				<div v-else class="space-y-6">
					<div v-for="note in filteredNotes" :key="note.id" class="p-6 hover:shadow-sm transition-shadow">
						<!-- Title and Date -->
						<div class="flex items-start justify-between mb-2">
							<h3 class="text-lg font-semibold text-primary hover:text-primary/80">
								<NuxtLink :to="`/notes/${note.id}`" class="hover:underline">
									<span v-html="highlightText(note.title, searchQuery)"></span>
								</NuxtLink>
							</h3>
							<div class="flex flex-col items-end text-sm text-muted ml-4 shrink-0">
								<p>{{ formatDate(note.createdAt) }}</p>
								<p v-if="note.meetingStartTime">{{ formatTime(note.meetingStartTime) }}</p>
							</div>
						</div>

						<!-- Content Preview -->
						<div class="text-sm text-muted mb-3 leading-relaxed">
							<span v-html="highlightText(truncateContent(note.content), searchQuery)"></span>
						</div>

						<!-- Metadata -->
						<div class="flex flex-wrap items-center gap-4 text-xs text-muted">
							<!-- Attendees -->
							<div v-if="note.attendees && note.attendees.length > 0" class="flex items-center gap-2">
								<UIcon name="i-heroicons-users" class="h-4 w-4" />
								<span>Attendees:</span>
								<div class="flex flex-wrap gap-1">
									<span v-for="attendee in note.attendees" :key="attendee" class="px-2 py-1 bg-muted/50 rounded text-xs" v-html="highlightText(attendee, searchQuery)"></span>
								</div>
							</div>

							<!-- Action Items -->
							<div v-if="note.actionItems && note.actionItems.length > 0" class="flex items-center gap-2">
								<UIcon :name="getActionItemsIcon(note.actionItems).icon" class="h-4 w-4" :class="getActionItemsIcon(note.actionItems).color" />
								<span>{{ completedActionItems(note.actionItems) }} of {{ note.actionItems.length }} action items completed</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Empty State -->
				<div v-if="!notesStore.loading.value && !notesStore.error.value && filteredNotes.length === 0" class="text-center py-12">
					<div class="text-muted">
						<UIcon name="i-heroicons-document-text" class="mx-auto h-16 w-16 mb-4 opacity-50" />
						<h3 class="text-xl font-medium mb-2">
							{{ searchQuery ? 'No notes found' : 'No notes yet' }}
						</h3>
						<p class="mb-4">
							{{ searchQuery ? 'Try adjusting your search terms or create a new note.' : 'Get started by creating your first note.' }}
						</p>
						<UButton to="/notes/create" icon="i-heroicons-plus">
							Create Your First Note
						</UButton>
					</div>
				</div>
			</div>
		</div>
	</UContainer>
</template>

<script setup lang="ts">
import type { Note } from '../../../model/Note'
import { useNotesStore } from '../../composables/stores/useNotesStore'

// Store instance
const notesStore = useNotesStore()

// Reactive state
const searchQuery = ref('')

// Filtered notes based on search query
const filteredNotes = computed(() => {
	const allNotes = notesStore.notes.value
	
	if (!searchQuery.value.trim()) {
		return allNotes
	}

	const query = searchQuery.value.toLowerCase()
	return allNotes.filter(note =>
		note.title.toLowerCase().includes(query) ||
		note.content.toLowerCase().includes(query) ||
		note.attendees?.some(attendee => attendee.toLowerCase().includes(query))
	)
})

// Load notes from backend
const loadNotes = async () => {
	try {
		await notesStore.search()
	} catch (err) {
		console.error('Failed to load notes:', err)
	}
}

// Load notes on mount
onMounted(() => {
	loadNotes()
})

// Format date for display
const formatDate = (date: Date) => {
	return new Intl.DateTimeFormat('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	}).format(new Date(date))
}

const formatTime = (date: Date) => {
	return new Intl.DateTimeFormat('en-US', {
		hour: 'numeric',
		minute: '2-digit'
	}).format(new Date(date))
}

// Truncate content for preview
const truncateContent = (content: string, maxLength = 200) => {
	if (content.length <= maxLength) return content
	return content.substring(0, maxLength) + '...'
}

// Highlight search terms in text
const highlightText = (text: string, searchTerm: string) => {
	if (!searchTerm || !text) return text

	const regex = new RegExp(`(${searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
	return text.replace(regex, '<mark class="text-warning dark:text-warning bg-elevated px-1 rounded">$1</mark>')
}

// Count completed action items
const completedActionItems = (actionItems: any[]) => {
	return actionItems.filter(item => item.completed).length
}

// Get action items completion status
const getActionItemsStatus = (actionItems: any[]) => {
	if (!actionItems || actionItems.length === 0) return 'none'

	const completed = completedActionItems(actionItems)
	const total = actionItems.length

	if (completed === 0) return 'none'
	if (completed === total) return 'all'
	return 'some'
}

// Get icon and color for action items status
const getActionItemsIcon = (actionItems: any[]) => {
	const status = getActionItemsStatus(actionItems)

	switch (status) {
		case 'none':
			return { icon: 'i-heroicons-x-circle', color: 'text-neutral' }
		case 'some':
			return { icon: 'i-heroicons-clock', color: 'text-warning' }
		case 'all':
			return { icon: 'i-heroicons-check-circle', color: 'text-success' }
		default:
			return { icon: 'i-heroicons-check-circle', color: 'text-neutral' }
	}
}

useHead({
	title: 'Notes'
})
</script>
