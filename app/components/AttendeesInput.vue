<template>
	<div class="flex flex-col space-y-2 flex-1 min-h-0">
		<!-- Add New Attendee -->
		<div class="flex gap-2">
			<UInput v-model="newAttendee" variant="soft" placeholder="Add attendee..." size="sm" @keyup.enter="addAttendee" class="flex-1" />
			<UButton size="sm" @click="addAttendee" :disabled="!newAttendee.trim()">
				Add
			</UButton>
		</div>

		<!-- Attendees List -->
		<div class="flex flex-wrap gap-2 overflow-y-auto flex-1 min-h-0">
			<div v-for="(attendee, index) in attendees" :key="index" class="flex items-center gap-2 bg-muted/50 px-3 py-1 rounded-sm text-sm">
				<span>{{ attendee }}</span>
				<UButton size="xs" variant="ghost" color="neutral" icon="i-heroicons-x-mark" @click="removeAttendee(index)" aria-label="Remove attendee" class="h-4 w-4 p-0 hover:bg-muted" />
			</div>
			<div v-if="attendees.length === 0" class="text-xs text-dimmed italic py-2">
				No attendees added yet. Add one above.
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
interface Props {
	modelValue?: string[]
}

const props = withDefaults(defineProps<Props>(), {
	modelValue: () => []
})

const emit = defineEmits<{
	'update:modelValue': [value: string[]]
}>()

const newAttendee = ref('')
const attendees = computed(() => props.modelValue || [])

// Add new attendee
const addAttendee = () => {
	if (!newAttendee.value.trim()) return

	const newAttendees = [
		...attendees.value,
		newAttendee.value.trim()
	]
	emit('update:modelValue', newAttendees)
	newAttendee.value = ''
}

// Remove attendee
const removeAttendee = (index: number) => {
	const newAttendees = attendees.value.filter((_, i) => i !== index)
	emit('update:modelValue', newAttendees)
}
</script>