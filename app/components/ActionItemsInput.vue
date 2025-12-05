<template>
	<div class="flex flex-col space-y-2 flex-1 min-h-0">
		<UTextarea v-model="actionItemsText" variant="soft" placeholder="Enter action items, one per line..." class="flex-1 min-h-0" @update:model-value="updateActionItems" />
		<div v-if="actionItems.length > 0" class="flex flex-col gap-2 mt-2 max-h-32 overflow-y-auto">
			<div v-for="(item, index) in actionItems" :key="index" class="flex items-start gap-2 text-sm">
				<span class="text-muted">•</span>
				<span>{{ item }}</span>
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

// Convert array to text (one per line)
const actionItemsText = computed({
	get: () => props.modelValue?.join('\n') || '',
	set: (value: string) => {
		const items = value
			.split('\n')
			.map(line => line.trim())
			.filter(line => line.length > 0)
		emit('update:modelValue', items)
	}
})

// Computed action items array for display
const actionItems = computed(() => props.modelValue || [])

// Update action items from textarea
const updateActionItems = () => {
	const items = actionItemsText.value
		.split('\n')
		.map(line => line.trim())
		.filter(line => line.length > 0)
	emit('update:modelValue', items)
}
</script>
