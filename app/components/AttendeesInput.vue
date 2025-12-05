<template>
	<div class="flex flex-col space-y-2 flex-1 min-h-0">
		<UTextarea v-model="attendeesText" variant="soft" placeholder="Enter attendees, one per line..." class="flex-1 min-h-0" @update:model-value="updateAttendees" />
		<div v-if="attendees.length > 0" class="flex flex-wrap gap-2 mt-2">
			<UBadge v-for="(attendee, index) in attendees" :key="index" variant="soft" color="neutral">
				{{ attendee }}
			</UBadge>
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

// Convert array to text (one per line)
const attendeesText = computed({
	get: () => props.modelValue?.join('\n') || '',
	set: (value: string) => {
		const attendees = value
			.split('\n')
			.map(line => line.trim())
			.filter(line => line.length > 0)
		emit('update:modelValue', attendees)
	}
})

// Computed attendees array for display
const attendees = computed(() => props.modelValue || [])

// Update attendees from textarea
const updateAttendees = () => {
	const attendees = attendeesText.value
		.split('\n')
		.map(line => line.trim())
		.filter(line => line.length > 0)
	emit('update:modelValue', attendees)
}
</script>
