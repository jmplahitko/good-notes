<template>
	<div class="flex flex-col">
		<!-- Action Items List -->
		<div class="flex flex-col gap-2 max-h-48 overflow-y-auto">
			<div v-for="(item, index) in actionItems" :key="index" class="flex items-start gap-2 text-sm group">
				<UCheckbox :model-value="item.completed" @update:model-value="(value: boolean | 'indeterminate') => toggleItem(index, value === true)" class="mt-0.5" :disabled="props.disabled" />
				<span :class="[
					'flex-1 pt-0.5',
					item.completed ? 'line-through text-muted' : ''
				]">
					{{ item.title }}
				</span>
				<UButton v-if="!props.disabled" size="xs" variant="ghost" color="error" icon="i-heroicons-trash" @click="removeItem(index)" aria-label="Remove action item"
					class="opacity-0 group-hover:opacity-100 transition-opacity" />
			</div>
			<p v-if="actionItems.length === 0" class="text-xs text-dimmed italic py-1">
				No action items added.
			</p>
		</div>

		<!-- Add New Action Item -->
		<Transition enter-active-class="transition-all duration-200 ease-out" enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0"
			leave-active-class="transition-all duration-150 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-2">
			<div v-if="!props.disabled" class="flex gap-2 mt-3 pt-3 border-t border-default">
				<UInput v-model="newItemText" variant="soft" placeholder="Add action item..." size="sm" @keyup.enter="addActionItem" class="flex-1" />
				<UButton size="sm" @click="addActionItem" :disabled="!newItemText.trim()">
					Add
				</UButton>
			</div>
		</Transition>
	</div>
</template>

<script setup lang="ts">
import type { ActionItem } from '../../model/ActionItem'

interface Props {
	modelValue?: ActionItem[]
	disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
	modelValue: () => [],
	disabled: false
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
