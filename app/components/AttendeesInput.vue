<template>
	<div class="flex flex-col">
		<!-- Attendees List -->
		<div class="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
			<div v-for="(attendee, index) in attendees" :key="index" class="flex items-center gap-1 bg-muted/50 px-3 py-1 rounded-sm text-sm group">
				<span>{{ attendee }}</span>
				<UButton v-if="!props.disabled" size="xs" variant="ghost" color="neutral" icon="i-heroicons-x-mark" @click="removeAttendee(index)" aria-label="Remove attendee"
					class="h-4 w-4 p-0 opacity-50 group-hover:opacity-100 transition-opacity" />
			</div>
			<p v-if="attendees.length === 0" class="text-xs text-dimmed italic py-1 w-full">
				No attendees added.
			</p>
		</div>

		<!-- Add New Attendee -->
		<Transition enter-active-class="transition-all duration-200 ease-out" enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0"
			leave-active-class="transition-all duration-150 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-2">
			<div v-if="!props.disabled" class="flex gap-2 mt-3 pt-3 border-t border-default">
				<UInput v-model="newAttendee" variant="soft" placeholder="Add attendee..." size="sm" @keyup.enter="addAttendee" class="flex-1" />
				<UButton size="sm" @click="addAttendee" :disabled="!newAttendee.trim()">
					Add
				</UButton>
			</div>
		</Transition>
	</div>
</template>

<script setup lang="ts">
interface Props {
	modelValue?: string[]
	disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
	modelValue: () => [],
	disabled: false
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
