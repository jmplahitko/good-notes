<template>
	<UContainer>
		<!-- Title and Meeting Time Row -->
		<div class="flex gap-4 items-center">
			<div class="flex-5">
				<UInput ref="titleInput" class="font-bold" v-model="pendingNote.title" variant="ghost" size="xl" label="Note Title" placeholder="Enter note title..." @update:model-value="updatePendingNote" />
			</div>
			<div class="flex-1">
				<UInput v-model="meetingTimeString" variant="ghost" type="time" label="Meeting Start Time" placeholder="HH:MM" @update:model-value="updateMeetingTime" />
			</div>
		</div>

		<USeparator class="my-4" />

		<div class="grid grid-cols-3 gap-4">
			<div class="col-span-2">
				<NoteEditor v-model="pendingNote.content" placeholder="Start writing your note..." @update:model-value="updatePendingNote" />

				<!-- Save Button -->
				<div class="flex justify-end gap-2 mt-4">
					<UButton variant="ghost" @click="cancel">Cancel</UButton>
					<UButton @click="saveNote" :disabled="!canSave">Save Note</UButton>
				</div>
				<!-- <pre><code>{{ JSON.stringify(pendingNote, null, 2) }}</code></pre> -->
			</div>
			<div class="flex flex-col gap-4">
				<div class="flex flex-col">
					<label class="text-sm font-semibold mb-2 block">Action Items</label>
					<ActionItemsInput v-model="pendingNote.actionItems" @update:model-value="updatePendingNote" />
				</div>
				<div class="flex flex-col">
					<label class="text-sm font-semibold mb-2 block">Attendees</label>
					<AttendeesInput v-model="pendingNote.attendees" @update:model-value="updatePendingNote" />
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

// Template ref for title input
const titleInput = ref<{ $el: HTMLElement } | null>(null)

// Focus title input on mount
onMounted(() => {
	nextTick(() => {
		const input = titleInput.value?.$el?.querySelector('input')
		input?.focus()
	})
})

// Get current time as HH:MM string
const getCurrentTimeString = () => {
	const now = new Date()
	const hours = now.getHours().toString().padStart(2, '0')
	const minutes = now.getMinutes().toString().padStart(2, '0')
	return `${hours}:${minutes}`
}

// Meeting time as string for time input (default to now)
const meetingTimeString = ref(getCurrentTimeString())

// Pending note state (exists in memory before save)
const pendingNote = ref<Partial<Note>>({
	title: '',
	content: '',
	actionItems: [],
	attendees: [],
	meetingStartTime: new Date()
})

// Computed to check if note can be saved
const canSave = computed(() => {
	return pendingNote.value.title && pendingNote.value.title.trim().length > 0
})

// Update meeting time
const updateMeetingTime = (value: string) => {
	if (value) {
		const [hours, minutes] = value.split(':')
		const date = new Date()
		if (hours && minutes) {
			date.setHours(parseInt(hours, 10))
			date.setMinutes(parseInt(minutes, 10))
			date.setSeconds(0)
			date.setMilliseconds(0)
			pendingNote.value.meetingStartTime = date
		}
	} else {
		pendingNote.value.meetingStartTime = undefined
	}
	updatePendingNote()
}

// Update pending note (for reactivity)
const updatePendingNote = () => {
	// This ensures reactivity is maintained
	// In a real implementation, this would update the store's pending note
}

// Save note
const saveNote = async () => {
	if (!canSave.value) return

	try {
		// Call store action to save note (backend validates and returns updated data)
		const savedNote = await notesStore.create(pendingNote.value)

		// Navigate to the created note with edit mode enabled
		await navigateTo(`/notes/${savedNote.id}?edit=true`)
	} catch (error) {
		// Error is handled by the store and displayed via reactive error state
		console.error('Failed to save note:', error)
		// TODO: Show user-friendly error message (toast notification, etc.)
	}
}

// Cancel
const cancel = () => {
	// TODO: Clear pending note from store
	// Clear local state
	pendingNote.value = {
		title: '',
		content: '',
		actionItems: [],
		attendees: []
	}
	meetingTimeString.value = ''

	// Navigate back
	navigateTo('/notes')
}

useHead({
	title: 'Create Note'
})
</script>
