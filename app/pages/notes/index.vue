<template>
	<UContainer>
		<div class="space-y-6">

			<!-- Search Section -->
			<div class="max-w-2xl mx-auto">
				<UInput v-model="searchQuery" variant="outline" size="lg" label="Search Notes" placeholder="Search by title, content, or attendees..." icon="i-heroicons-magnifying-glass"
					@update:model-value="performSearch" />
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

				<!-- Search Results (Google-style) -->
				<div class="space-y-6">
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
							<span v-html="highlightText(note.content, searchQuery)"></span>
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
								<UIcon name="i-heroicons-check-circle" class="h-4 w-4" />
								<span>{{ completedActionItems(note.actionItems) }} of {{ note.actionItems.length }} action items completed</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Empty State -->
				<div v-if="filteredNotes.length === 0" class="text-center py-12">
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

// Mock notes data
const mockNotes: Note[] = [
	{
		id: 'note-1',
		title: 'Team Standup Meeting',
		content: 'Discussed project progress and upcoming deadlines. Key points: API integration is on track, UI improvements needed for mobile responsiveness.',
		createdAt: new Date('2024-12-01T09:00:00'),
		updatedAt: new Date('2024-12-01T09:30:00'),
		meetingStartTime: new Date('2024-12-01T09:00:00'),
		attendees: ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson'],
		actionItems: [
			{ title: 'Fix mobile responsiveness', completed: false },
			{ title: 'Update API documentation', completed: true },
			{ title: 'Review pull requests', completed: false }
		]
	},
	{
		id: 'note-2',
		title: 'Client Presentation Prep',
		content: 'Prepared slides for quarterly business review. Focus on Q4 achievements and Q1 roadmap. Client expressed interest in expanded features.',
		createdAt: new Date('2024-11-28T14:00:00'),
		updatedAt: new Date('2024-11-28T16:00:00'),
		meetingStartTime: new Date('2024-11-28T14:30:00'),
		attendees: ['Alice Johnson', 'Eve Martinez'],
		actionItems: [
			{ title: 'Create presentation slides', completed: true },
			{ title: 'Gather Q4 metrics', completed: true },
			{ title: 'Schedule follow-up meeting', completed: false }
		]
	},
	{
		id: 'note-3',
		title: 'Code Review Session',
		content: 'Reviewed recent code changes for the authentication module. Identified several security improvements and performance optimizations.',
		createdAt: new Date('2024-11-25T11:00:00'),
		updatedAt: new Date('2024-11-25T12:30:00'),
		meetingStartTime: new Date('2024-11-25T11:15:00'),
		attendees: ['Bob Smith', 'David Wilson', 'Frank Garcia'],
		actionItems: [
			{ title: 'Implement security fixes', completed: false },
			{ title: 'Add performance optimizations', completed: false },
			{ title: 'Update code documentation', completed: true }
		]
	},
	{
		id: 'note-4',
		title: 'Product Planning Meeting',
		content: 'Brainstormed new features for Q1. Prioritized user experience improvements and mobile app enhancements.',
		createdAt: new Date('2024-11-20T10:00:00'),
		updatedAt: new Date('2024-11-20T11:30:00'),
		meetingStartTime: new Date('2024-11-20T10:30:00'),
		attendees: ['Alice Johnson', 'Carol Davis', 'Eve Martinez', 'Grace Lee'],
		actionItems: [
			{ title: 'Create feature roadmap', completed: true },
			{ title: 'Design mobile improvements', completed: false },
			{ title: 'User research interviews', completed: false }
		]
	},
	{
		id: 'note-5',
		title: 'Bug Triage',
		content: 'Reviewed reported bugs and prioritized fixes. Critical security issue identified and assigned to development team.',
		createdAt: new Date('2024-11-18T15:00:00'),
		updatedAt: new Date('2024-11-18T16:00:00'),
		meetingStartTime: new Date('2024-11-18T15:45:00'),
		attendees: ['Bob Smith', 'David Wilson'],
		actionItems: [
			{ title: 'Fix critical security bug', completed: true },
			{ title: 'Update bug tracking system', completed: false },
			{ title: 'Review remaining bug reports', completed: false }
		]
	}
]

// Reactive state
const searchQuery = ref('')
const filteredNotes = ref<Note[]>(mockNotes)

// Search functionality
const performSearch = () => {
	if (!searchQuery.value.trim()) {
		filteredNotes.value = mockNotes
		return
	}

	const query = searchQuery.value.toLowerCase()
	filteredNotes.value = mockNotes.filter(note =>
		note.title.toLowerCase().includes(query) ||
		note.content.toLowerCase().includes(query) ||
		note.attendees?.some(attendee => attendee.toLowerCase().includes(query))
	)
}

// Format date for display
const formatDate = (date: Date) => {
	return new Intl.DateTimeFormat('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	}).format(date)
}

const formatTime = (date: Date) => {
	return new Intl.DateTimeFormat('en-US', {
		hour: 'numeric',
		minute: '2-digit'
	}).format(date)
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

// Confirm delete (placeholder)
const confirmDelete = (note: Note) => {
	// TODO: Implement delete functionality
	console.log('Delete note:', note.id)
	// For now, just remove from local array
	filteredNotes.value = filteredNotes.value.filter(n => n.id !== note.id)
}

useHead({
	title: 'Notes'
})
</script>