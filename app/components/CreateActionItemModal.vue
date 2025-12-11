<template>
	<UButton icon="i-heroicons-document-check" aria-label="Create Action Item" color="neutral" variant="ghost" @click="isOpen = true" />
	<UModal :open="isOpen" @update:open="isOpen = $event">
		<template #body>
			<form @submit.prevent="createActionItem" class="space-y-4">
				<UInput ref="title" :autofocus="true" variant="ghost" size="xl" v-model="formData.title" placeholder="What do you need to do?" required />

				<div class="flex items-center gap-2 pl-4">
					<UCheckbox v-model="formData.completed" />
					<span class="text-sm">Completed</span>
				</div>

				<div class="flex justify-end gap-3 pt-4">
					<div class="flex items-center gap-2">
						<UCheckbox v-model="shouldMakeAnotherActionItem" />
						<span class="text-sm">Make another</span>
					</div>
					<UButton type="submit" :disabled="!formData.title.trim()" :loading="loading">
						Create Action Item
					</UButton>
				</div>
			</form>
		</template>
	</UModal>
</template>

<script setup lang="ts">
import { useActionItemsStore } from '../composables/stores/useActionItemsStore'

// Get the action items store
const actionItemsStore = useActionItemsStore()

const isOpen = ref(false);

const title = ref<{ $el: HTMLElement } | null>(null)

const formData = ref({
	title: '',
	noteId: '',
	completed: false
})

const shouldMakeAnotherActionItem = ref(false);

// Reactive state from store
const { loading, error } = actionItemsStore

// Hotkey handler for Cmd+A (Mac) or Ctrl+A (Windows/Linux)
// Opens the create action item modal
const handleKeydown = (event: KeyboardEvent) => {
	if ((event.metaKey || event.ctrlKey) && event.key === 'a') {
		event.preventDefault() // Prevent default "select all" behavior
		isOpen.value = true
	}
}

// Add/remove keyboard event listener
onMounted(() => {
	document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
	document.removeEventListener('keydown', handleKeydown)
})

// Create action item
const createActionItem = async () => {
	if (!formData.value.title.trim()) return

	try {
		await actionItemsStore.create({
			title: formData.value.title,
			noteId: formData.value.noteId || undefined
		})

		if (shouldMakeAnotherActionItem.value) {
			reset()
		} else {
			isOpen.value = false
			reset()
		}
	} catch (error) {
		console.error('Failed to create action item:', error)
		// Error is handled by the store and can be displayed in the UI
	}
}

// Reset form
const reset = () => {
	formData.value = {
		title: '',
		noteId: '',
		completed: false
	}

	title?.value?.$el?.querySelector('input')?.focus();
}
</script>
