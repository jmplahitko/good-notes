<template>
	<UContainer>
		<!-- Title and Meeting Time Row -->
		<div class="flex gap-4 items-center">
			<div class="flex-5">
				<UInput v-model="noteTitle" variant="ghost" size="xl" label="Note Title" placeholder="Enter note title..." />
			</div>
			<div class="flex-1">
				<UInput v-model="meetingTimeString" variant="ghost" type="time" label="Meeting Start Time" placeholder="HH:MM" @update:model-value="updateMeetingTime" />
			</div>
		</div>

		<USeparator class="my-4" />

		<div class="grid grid-cols-3 gap-4">
			<div class="col-span-2">
				<NoteEditor v-model="noteContent" placeholder="Start writing your note..." />

				<!-- Action Buttons -->
				<div class="flex justify-between items-center mt-4">
					<UButton variant="outline" @click="revertChanges" :disabled="notesStore.loading.value">
						Revert Changes
					</UButton>
					<div class="flex gap-2">
						<UButton variant="ghost" @click="cancel">Cancel</UButton>
						<UButton @click="saveNote" :disabled="!canSave" :loading="notesStore.loading.value">
							Save Changes
						</UButton>
					</div>
				</div>
			</div>
			<div>
				<label class="text-sm font-semibold mb-2 block">Action Items</label>
				<ActionItemsInput v-model="noteActionItems" />
				<label class="text-sm font-semibold mb-2 block">Attendees</label>
				<AttendeesInput v-model="noteAttendees" />
			</div>
		</div>
	</UContainer>
</template>

<script setup lang="ts">
import type { Note } from '../../../model/Note'
import type { ActionItem } from '../../../model/ActionItem'
import { useNotesStore } from '../../composables/stores/useNotesStore'

// Define route middleware
definePageMeta({
	middleware: 'get-note'
})

// Store instance
const notesStore = useNotesStore()

// Local copy of note for editing (deep copy breaks readonly reference from store)
const note = ref<Note | null>(null)

// Meeting time as string for time input
const meetingTimeString = ref('')

// Computed properties for v-model bindings (handle null case)
const noteTitle = computed({
	get: () => note.value?.title || '',
	set: (value: string) => {
		if (note.value) {
			note.value.title = value
		}
	}
})

const noteContent = computed({
	get: () => note.value?.content || '',
	set: (value: string) => {
		if (note.value) {
			note.value.content = value
		}
	}
})

const noteActionItems = computed({
	get: () => note.value?.actionItems || [],
	set: (value: ActionItem[]) => {
		if (note.value) {
			note.value.actionItems = value
		}
	}
})

const noteAttendees = computed({
	get: () => note.value?.attendees || [],
	set: (value: string[]) => {
		if (note.value) {
			note.value.attendees = value
		}
	}
})

// Computed to check if note can be saved
const canSave = computed(() => {
	return note.value?.title && note.value.title.trim().length > 0
})

// Update meeting time
const updateMeetingTime = (value: string) => {
	if (value && note.value) {
		const [hours, minutes] = value.split(':')
		const date = new Date()
		if (hours && minutes) {
			date.setHours(parseInt(hours, 10))
			date.setMinutes(parseInt(minutes, 10))
			date.setSeconds(0)
			date.setMilliseconds(0)
			note.value.meetingStartTime = date
		}
	} else if (note.value) {
		note.value.meetingStartTime = undefined
	}
}

// Update note (trigger reactivity)
const updateNote = () => {
	// Note updates are handled reactively through the computed property
	// The actual save happens in saveNote()
}

// Save note
const saveNote = async () => {
	if (!canSave.value || !note.value) return

	try {
		// Call store action to update note
		await notesStore.update(note.value.id, {
			title: note.value.title,
			content: note.value.content,
			actionItems: note.value.actionItems,
			attendees: note.value.attendees,
			meetingStartTime: note.value.meetingStartTime
		})

		// Navigate back to notes list or stay on page
		// For now, just show success (could add toast notification later)
		console.log('Note updated successfully')
	} catch (error) {
		// Error is handled by the store
		console.error('Failed to update note:', error)
	}
}

// Cancel - navigate back
const cancel = () => {
	navigateTo('/notes')
}


// Initialize meeting time string from note
const initializeMeetingTime = () => {
	if (note.value?.meetingStartTime) {
		const date = new Date(note.value.meetingStartTime)
		const hours = date.getHours().toString().padStart(2, '0')
		const minutes = date.getMinutes().toString().padStart(2, '0')
		meetingTimeString.value = `${hours}:${minutes}`
	} else {
		meetingTimeString.value = ''
	}
}

// Revert changes back to original note
const revertChanges = () => {
	if (notesStore.currentNote.value) {
		note.value = JSON.parse(JSON.stringify(notesStore.currentNote.value))
		initializeMeetingTime()
	}
}

// Initialize local note copy when store's currentNote loads
watchEffect(() => {
	if (notesStore.currentNote.value && !note.value) {
		// Create deep copy to break reference from store
		note.value = JSON.parse(JSON.stringify(notesStore.currentNote.value))
		initializeMeetingTime()
	}
})

useHead({
	title: 'Edit Note'
})
</script>
