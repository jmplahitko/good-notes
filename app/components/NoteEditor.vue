<template>
	<div class="rounded-sm">
		<!-- Toolbar -->
		<div class="flex">
			<div class="flex items-center gap-1 p-2 border border-default rounded-sm" v-if="!isDisabled">
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('bold') }" @click="editor?.chain().focus().toggleBold().run()" :icon="'i-heroicons-bold'"
					aria-label="Bold" />
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('italic') }" @click="editor?.chain().focus().toggleItalic().run()" :icon="'i-heroicons-italic'"
					aria-label="Italic" />
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('strike') }" @click="editor?.chain().focus().toggleStrike().run()" :icon="'i-heroicons-bars-3'"
					aria-label="Strikethrough" />
				<div class="w-px h-4 bg-accented mx-1" />
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('heading', { level: 2 }) }" @click="editor?.chain().focus().toggleHeading({ level: 2 }).run()"
					:icon="'i-heroicons-h2'" aria-label="Heading 2" />
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('heading', { level: 3 }) }" @click="editor?.chain().focus().toggleHeading({ level: 3 }).run()"
					:icon="'i-heroicons-h3'" aria-label="Heading 3" />
				<div class="w-px h-4 bg-accented mx-1" />
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('bulletList') }" @click="editor?.chain().focus().toggleBulletList().run()"
					:icon="'i-heroicons-list-bullet'" aria-label="Bullet List" />
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('orderedList') }" @click="editor?.chain().focus().toggleOrderedList().run()"
					:icon="'i-heroicons-numbered-list'" aria-label="Numbered List" />
				<UButton size="xs" variant="ghost" color="neutral" :class="{ 'bg-primary/20': editor?.isActive('blockquote') }" @click="editor?.chain().focus().toggleBlockquote().run()"
					:icon="'i-heroicons-chat-bubble-left-right'" aria-label="Quote" />
				<div class="w-px h-4 bg-accented mx-1" />
				<UButton size="xs" variant="ghost" color="neutral" @click="editor?.chain().focus().setHorizontalRule().run()" :icon="'i-heroicons-minus'" aria-label="Horizontal Rule" />
				<UButton size="xs" variant="ghost" color="neutral" @click="editor?.chain().focus().undo().run()" :icon="'i-heroicons-arrow-uturn-left'" aria-label="Undo" :disabled="!editor?.can().undo()" />
				<UButton size="xs" variant="ghost" color="neutral" @click="editor?.chain().focus().redo().run()" :icon="'i-heroicons-arrow-uturn-right'" aria-label="Redo" :disabled="!editor?.can().redo()" />
			</div>
			<p v-else class="flex items-center pl-2 text-sm text-dimmed italic">Unlock editor to modify content.</p>
			<div class="ml-auto flex items-center gap-1 p-2">
				<UButton size="xs" variant="ghost" color="neutral" @click="toggleDisabled" :icon="isDisabled ? 'i-heroicons-lock-closed' : 'i-heroicons-lock-open'" aria-label="Toggle Editor Lock" />
			</div>
		</div>

		<!-- Editor Content -->
		<EditorContent :editor="editor" class="mt-4 prose prose-sm max-w-none dark:prose-invert" />

		<!-- Character Count -->
		<div class="flex items-center justify-end px-3 py-1 text-xs text-muted">
			<p>{{ editor?.storage.characterCount.characters() }} characters</p>
		</div>
	</div>
</template>

<script setup lang="ts">
// @ts-ignore - TipTap types not available during development
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import CharacterCount from '@tiptap/extension-character-count'

interface Props {
	modelValue?: string
	placeholder?: string
	disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
	modelValue: '',
	placeholder: 'Start writing...',
	disabled: false
})

const emit = defineEmits<{
	'update:modelValue': [value: string]
	'update:disabled': [value: boolean]
}>()

// Local reactive state for disabled state (can be controlled by prop or local state)
const isDisabled = ref(props.disabled)

// Watch for prop changes
watch(() => props.disabled, (newValue) => {
	isDisabled.value = newValue
})

const editor = ref<Editor>()

onMounted(() => {
	editor.value = new Editor({
		content: props.modelValue,
		editable: !isDisabled.value,
		extensions: [
			StarterKit,
			Placeholder.configure({
				placeholder: props.placeholder,
			}),
			CharacterCount,
		],
		onUpdate: ({ editor }) => {
			if (!isDisabled.value) {
				emit('update:modelValue', editor.getHTML())
			}
		},
		editorProps: {
			attributes: {
				class: 'min-h-[200px] focus:outline-none',
			},
		},
	})
})

onUnmounted(() => {
	editor.value?.destroy()
})

// Watch for external content changes
watch(() => props.modelValue, (newContent) => {
	if (editor.value && newContent !== editor.value.getHTML()) {
		editor.value.commands.setContent(newContent)
	}
})

// Watch for prop changes
watch(() => props.disabled, (newValue) => {
	isDisabled.value = newValue
})

// Toggle disabled state
const toggleDisabled = () => {
	isDisabled.value = !isDisabled.value
	emit('update:disabled', isDisabled.value)
}

// Watch for disabled state changes
watch(isDisabled, (newDisabled) => {
	if (editor.value) {
		editor.value.setEditable(!newDisabled)
	}
})

// Expose editor for parent components if needed
defineExpose({
	editor,
	getHTML: () => editor.value?.getHTML(),
	getText: () => editor.value?.getText(),
	getJSON: () => editor.value?.getJSON(),
})
</script>

<style>
@reference '../assets/css/main.css';

/* TipTap Prose Styles */
.tiptap {
	@apply w-full rounded-md border-0 appearance-none placeholder:text-dimmed focus:outline-none transition-colors text-toned bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 px-2.5 py-1.5 text-sm gap-1.5;
}

.tiptap[contenteditable="false"] {
	@apply cursor-default;
	@apply bg-default;
}

.prose {
	color: var(--ui-text);
}

.prose h1 {
	color: var(--ui-text-highlighted);
	font-size: 2em;
	font-weight: 700;
	margin-top: 0;
	margin-bottom: 0.5em;
}

.prose h2 {
	color: var(--ui-text-highlighted);
	font-size: 1.5em;
	font-weight: 600;
	margin-top: 0.83em;
	margin-bottom: 0.5em;
}

.prose h3 {
	color: var(--ui-text-highlighted);
	font-size: 1.25em;
	font-weight: 600;
	margin-top: 1em;
	margin-bottom: 0.5em;
}

.prose p {
	margin-top: 0.75em;
	margin-bottom: 0.75em;
}

.prose ul,
.prose ol {
	padding-left: 1.5em;
	margin: 0.5em 0;
}

.prose li {
	margin: 0 0;
}

.prose ul li {
	list-style-type: disc;
}

.prose ol li {
	list-style-type: decimal;
}

.prose li p {
	margin: 0;
}

.prose blockquote {
	border-left: 4px solid var(--ui-border-accented);
	padding-left: 1em;
	margin: 1em 0;
	font-style: italic;
	color: var(--ui-text-muted);
}

.prose code {
	background-color: var(--ui-bg-accented);
	color: var(--ui-text-highlighted);
	padding: 0.125em 0.25em;
	border-radius: 0.25em;
	font-size: 0.875em;
}

.prose pre {
	background-color: var(--ui-bg-accented);
	color: var(--ui-text-highlighted);
	padding: 1em;
	border-radius: 0.375em;
	overflow-x: auto;
	margin: 1em 0;
}

.prose pre code {
	background: none;
	padding: 0;
	border-radius: 0;
}

.prose hr {
	border-color: var(--ui-border);
	margin: 1.5em 0;
}

.prose strong {
	font-weight: 900;
}

.prose em {
	font-style: italic;
}

.prose del {
	text-decoration: line-through;
}

/* Focus styles for editor content */
.ProseMirror-focused {
	outline: none;
}

.ProseMirror p.is-editor-empty:first-child::before {
	color: var(--ui-text-dimmed);
	content: attr(data-placeholder);
	float: left;
	height: 0;
	pointer-events: none;
}
</style>
