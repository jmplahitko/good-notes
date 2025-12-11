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
					<UButton type="submit" :disabled="!formData.title.trim()">
						Create Action Item
					</UButton>
				</div>
			</form>
		</template>
	</UModal>
</template>

<script setup lang="ts">
import { useActionItems } from '../composables/useActionItems'

// Get the action items composable
const { addActionItem } = useActionItems()

const isOpen = ref(false);

const title = ref<{ $el: HTMLElement } | null>(null)

const formData = ref({
	title: '',
	noteId: '',
	completed: false
})

const shouldMakeAnotherActionItem = ref(false);

// Create action item
const createActionItem = () => {
	if (!formData.value.title.trim()) return

	// Add the action item using the composable
	addActionItem({
		title: formData.value.title,
		noteId: formData.value.noteId || undefined,
		completed: formData.value.completed,
		completedAt: formData.value.completed ? new Date() : null
	})

	if (shouldMakeAnotherActionItem.value) {
		reset()
	} else {
		isOpen.value = false;
	}

	// Reset form
	reset()
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
