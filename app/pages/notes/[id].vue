<template>
	<UContainer>
		<!-- Title and Meeting Time Row -->
		<div class="flex gap-4 items-center">
			<div class="flex-5">
				<UInput v-model="noteTitle" variant="ghost" size="xl" label="Note Title" placeholder="Enter note title..." :disabled="!isEditing" />
			</div>
			<div class="flex-1">
				<UInput v-model="meetingTimeString" variant="ghost" type="time" label="Meeting Start Time" placeholder="HH:MM" @update:model-value="updateMeetingTime" :disabled="!isEditing" />
			</div>
		</div>

		<USeparator class="my-4" />

		<div class="grid grid-cols-3 gap-4">
			<div class="col-span-2">
				<NoteEditor v-model="noteContent" placeholder="Start writing your note..." :disabled="!isEditing" />

				<!-- Action Buttons -->
				<div class="flex justify-between items-center mt-4">
					<!-- Left side -->
					<div>
						<UButton v-if="isEditing" variant="outline" @click="revertChanges" :disabled="notesStore.loading.value">
							Revert Changes
						</UButton>
					</div>

					<!-- Right side -->
					<div class="flex gap-2">
						<template v-if="isEditing">
							<UButton variant="ghost" @click="cancelEditing">Cancel</UButton>
							<UButton @click="saveNote" :disabled="!canSave" :loading="notesStore.loading.value">
								Save Changes
							</UButton>
						</template>
						<template v-else>
							<UButton variant="ghost" @click="goBack">Back to Notes</UButton>
							<UButton @click="startEditing" icon="i-heroicons-pencil">
								Edit Note
							</UButton>
						</template>
					</div>
				</div>
			</div>
			<div class="space-y-6">
				<div>
					<label class="text-sm font-semibold mb-2 block">Action Items</label>
					<ActionItemsInput v-model="noteActionItems" :disabled="!isEditing" />
				</div>
				<div>
					<label class="text-sm font-semibold mb-2 block">Attendees</label>
					<AttendeesInput v-model="noteAttendees" :disabled="!isEditing" />
				</div>
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

// Store and route
const notesStore = useNotesStore()
const route = useRoute()

// Editing state - locked by default unless ?edit=true
const isEditing = ref(false)

// Local copy of note for editing (deep copy breaks readonly reference from store)
const note = ref<Note | null>(null)

// Meeting time as string for time input
const meetingTimeString = ref('')

// Check for edit query param on mount
onMounted(() => {
	if (route.query.edit === 'true') {
		isEditing.value = true
		// Remove the query param from URL without navigation
		const newQuery = { ...route.query }
		delete newQuery.edit
		navigateTo({ path: route.path, query: newQuery }, { replace: true })
	}
})

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

// Start editing
const startEditing = () => {
	isEditing.value = true
}

// Cancel editing - revert changes and lock
const cancelEditing = () => {
	revertChanges()
	isEditing.value = false
}

// Go back to notes list
const goBack = () => {
	navigateTo('/notes')
}

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

		// Lock the editor after successful save
		isEditing.value = false
		console.log('Note updated successfully')
	} catch (error) {
		// Error is handled by the store
		console.error('Failed to update note:', error)
	}
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
	title: computed(() => isEditing.value ? 'Edit Note' : 'View Note')
})
</script>
