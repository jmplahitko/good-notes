<template>
	<div class="flex flex-col space-y-2 flex-1 min-h-0">
		<!-- Add New Action Item -->
		<div class="flex gap-2">
			<UInput v-model="newItemText" variant="soft" placeholder="Add action item..." size="sm" @keyup.enter="addActionItem" class="flex-1" />
			<UButton size="sm" @click="addActionItem" :disabled="!newItemText.trim()">
				Add
			</UButton>
		</div>

		<!-- Action Items List -->
		<div class="flex flex-col gap-2 overflow-y-auto flex-1 min-h-0">
			<div v-for="(item, index) in actionItems" :key="index" class="flex items-start gap-2 text-sm">
				<UCheckbox :model-value="item.completed" @update:model-value="(value: boolean | 'indeterminate') => toggleItem(index, value === true)" class="mt-0.5" />
				<span :class="[
					'flex-1 pt-0.5',
					item.completed ? 'line-through text-muted' : ''
				]">
					{{ item.title }}
				</span>
				<UButton size="xs" variant="ghost" color="error" icon="i-heroicons-trash" @click="removeItem(index)" aria-label="Remove action item" />
			</div>
			<div v-if="actionItems.length === 0" class="text-xs text-dimmed italic py-2">
				No action items yet. Add one above.
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import type { ActionItem } from '../../model/ActionItem'

interface Props {
	modelValue?: ActionItem[]
}

const props = withDefaults(defineProps<Props>(), {
	modelValue: () => []
})

const emit = defineEmits<{
	'update:modelValue': [value: ActionItem[]]
}>()

const newItemText = ref('')

const actionItems = computed(() => props.modelValue || [])

// Add new action item
const addActionItem = () => {
	if (!newItemText.value.trim()) return

	const newItems = [
		...actionItems.value,
		{
			title: newItemText.value.trim(),
			completed: false
		}
	]
	emit('update:modelValue', newItems)
	newItemText.value = ''
}

// Toggle item completion
const toggleItem = (index: number, completed: boolean) => {
	const newItems = [...actionItems.value]
	if (newItems[index]) {
		newItems[index] = {
			...newItems[index],
			completed
		} as ActionItem
		emit('update:modelValue', newItems)
	}
}

// Remove item
const removeItem = (index: number) => {
	const newItems = actionItems.value.filter((_, i) => i !== index)
	emit('update:modelValue', newItems)
}
</script>
