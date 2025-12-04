<template>
	<div class="container mx-auto px-4 py-8 max-w-6xl">
		<UPageHero title="Design System Review" description="Dark Theme Design System" />

		<!-- Colors Section -->
		<UPageSection id="colors" title="Colors" class="">
			<div class="space-y-8">
				<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
					<div class="space-y-2">
						<div class="h-20 rounded border bg-primary"></div>
						<p class="text-sm">Primary</p>
						<p class="text-xs text-muted">#0e639c</p>
					</div>
					<div class="space-y-2">
						<div class="h-20 rounded border bg-secondary"></div>
						<p class="text-sm">Secondary</p>
						<p class="text-xs text-muted">#264f78</p>
					</div>
				</div>
				<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
					<div class="space-y-2">
						<div class="h-20 rounded border bg-info"></div>
						<p class="text-sm">Info</p>
						<p class="text-xs text-muted">#264f78</p>
					</div>
					<div class="space-y-2">
						<div class="h-20 rounded border bg-success"></div>
						<p class="text-sm">Success</p>
						<p class="text-xs text-muted">#1a975f</p>
					</div>
					<div class="space-y-2">
						<div class="h-20 rounded border bg-warning"></div>
						<p class="text-sm">Warning</p>
						<p class="text-xs text-muted">#cca700</p>
					</div>
					<div class="space-y-2">
						<div class="h-20 rounded border bg-error"></div>
						<p class="text-sm">Error</p>
						<p class="text-xs text-muted">#f48771</p>
					</div>
				</div>
				<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
					<div class="space-y-2">
						<div class="h-20 rounded border bg-black"></div>
						<p class="text-sm">Black</p>
						<p class="text-xs text-muted">#1e1e1e</p>
					</div>
					<div class="space-y-2">
						<div class="h-20 rounded border bg-gray-500"></div>
						<p class="text-sm">Gray</p>
						<p class="text-xs text-muted">#3c3c3c</p>
					</div>
					<div class="space-y-2">
						<div class="h-20 rounded border bg-white"></div>
						<p class="text-sm">White</p>
						<p class="text-xs text-muted">#cccccc</p>
					</div>
				</div>
			</div>
		</UPageSection>


		<UPageSection id="background-colors" title="Background Colors" class="">
			<div class="space-y-8">
				<div class="grid grid-cols-2 md:grid-cols-5 gap-4">
					<div class="flex items-center justify-center h-10 rounded-md border border-default bg-default">
						<p class="text-sm">Default</p>
					</div>
					<div class="flex items-center justify-center h-10 rounded-md border border-default bg-muted">
						<p class="text-sm">Muted</p>
					</div>
					<div class="flex items-center justify-center h-10 rounded-md border border-default bg-elevated">
						<p class="text-sm">Elevated</p>
					</div>
					<div class="flex items-center justify-center h-10 rounded-md border border-default bg-accented">
						<p class="text-sm">Accented</p>
					</div>
					<div class="flex items-center justify-center h-10 rounded-md border border-default bg-inverted">
						<p class="text-sm text-inverted">Inverted</p>
					</div>
				</div>
			</div>
		</UPageSection>

		<UPageSection id="border-colors" title="Border Colors" class="">
			<div class="space-y-8">
				<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
					<div class="flex items-center justify-center h-10 rounded-md border border-default">
						<p class="text-sm">Default</p>
					</div>
					<div class="flex items-center justify-center h-10 rounded-md border border-muted">
						<p class="text-sm">Muted</p>
					</div>
					<div class="flex items-center justify-center h-10 rounded-md border border-accented">
						<p class="text-sm">Accented</p>
					</div>
					<div class="flex items-center justify-center h-10 rounded-md border border-inverted">
						<p class="text-sm">Inverted</p>
					</div>
				</div>
			</div>
		</UPageSection>

		<!-- Typography Section -->
		<UPageSection id="typography" title="Typography" class="">
			<div class="space-y-6">
				<div>
					<h1 class="text-4xl font-bold mb-2">Heading 1</h1>
					<h2 class="text-3xl font-semibold mb-2">Heading 2</h2>
					<h3 class="text-2xl font-semibold mb-2">Heading 3</h3>
					<h4 class="text-xl font-semibold mb-2">Heading 4</h4>
					<h5 class="text-lg font-semibold mb-2">Heading 5</h5>
					<h6 class="text-base font-semibold mb-2">Heading 6</h6>
				</div>
				<div>
					<p class="text-base mb-2">Body text - Regular paragraph text for content.</p>
					<p class="text-sm text-muted mb-2">Small text - Muted text for secondary information.</p>
					<p class="text-xs text-toned">Extra small text - For captions and labels.</p>
				</div>
			</div>
		</UPageSection>

		<!-- Buttons Section -->
		<UPageSection id="buttons" title="Buttons" class="">
			<div class="space-y-6">
				<div>
					<h3 class="text-lg font-semibold mb-4">Button Variants</h3>
					<div class="flex flex-wrap gap-4">
						<UButton>Default</UButton>
						<UButton color="primary">Primary</UButton>
						<UButton color="gray">Gray</UButton>
						<UButton variant="outline">Outline</UButton>
						<UButton variant="ghost">Ghost</UButton>
						<UButton variant="soft">Soft</UButton>
					</div>
				</div>
				<div>
					<h3 class="text-lg font-semibold mb-4">Button Sizes</h3>
					<div class="flex flex-wrap items-center gap-4">
						<UButton size="xs">Extra Small</UButton>
						<UButton size="sm">Small</UButton>
						<UButton size="md">Medium</UButton>
						<UButton size="lg">Large</UButton>
						<UButton size="xl">Extra Large</UButton>
					</div>
				</div>
				<div>
					<h3 class="text-lg font-semibold mb-4">Button States</h3>
					<div class="flex flex-wrap gap-4">
						<UButton>Normal</UButton>
						<UButton disabled>Disabled</UButton>
						<UButton loading>Loading</UButton>
					</div>
				</div>
			</div>
		</UPageSection>

		<!-- Forms Section -->
		<UPageSection id="forms" title="Forms" class="">
			<div>
				<h3 class="text-lg font-semibold mb-4">Input Fields</h3>
				<div class="flex flex-col space-y-4">
					<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
						<UInput variant="outline" v-model="formData.text" label="Text Input" placeholder="Enter text" />
						<UInput variant="soft" v-model="formData.text" label="Text Input" placeholder="Enter text" />
						<UInput variant="subtle" v-model="formData.text" label="Text Input" placeholder="Enter text" />
						<UInput variant="ghost" v-model="formData.text" label="Text Input" placeholder="Enter text" />
					</div>
					<UInput variant="soft" v-model="formData.email" type="email" label="Email Input" placeholder="email@example.com" />
					<UInput variant="soft" v-model="formData.password" type="password" label="Password Input" />
					<UTextarea variant="soft" v-model="formData.textarea" label="Textarea" placeholder="Enter multiple lines" />
					<USelect variant="soft" v-model="formData.select" :items="selectOptions" label="Select" placeholder="Choose an option" />
					<UCheckbox variant="soft" v-model="formData.checkbox" label="Checkbox Option" />
					<URadioGroup variant="soft" v-model="formData.radio" :items="radioOptions" label="Radio Group" />
				</div>
			</div>

			<!-- Rich Text Editor Demo -->
			<div class="mt-8">
				<h3 class="text-lg font-semibold mb-4">Rich Text Editor</h3>
				<div class="max-w-2xl">
					<NoteEditor v-model="richTextContent" v-model:disabled="rteDisabled" placeholder="Start writing your note..." />
					<div class="mt-4 p-3 text-sm">
						<strong>HTML Output:</strong><br>
						<pre class="html-output"><code>{{ prettyPrintHtml(richTextContent) }}</code></pre>
					</div>
				</div>
			</div>
		</UPageSection>

		<!-- Cards Section -->
		<UPageSection id="cards" title="Cards" class="mt-12">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<UCard>
					<template #header>
						<h3 class="text-lg font-semibold">Card Title</h3>
					</template>
					<p>Card content goes here. This is a basic card component with header and content sections.</p>
					<template #footer>
						<div class="flex gap-2">
							<UButton size="sm">Action</UButton>
							<UButton size="sm" variant="ghost">Cancel</UButton>
						</div>
					</template>
				</UCard>
				<UCard>
					<p>Simple card without header or footer. Just content.</p>
				</UCard>
			</div>
		</UPageSection>

		<!-- Alerts Section -->
		<UPageSection id="alerts" title="Alerts" class="mt-12">
			<div class="space-y-4 max-w-2xl">
				<UAlert icon="i-heroicons-information-circle" color="blue" variant="soft" title="Info Alert" description="This is an informational alert message." />
				<UAlert icon="i-heroicons-check-circle" color="green" variant="soft" title="Success Alert" description="Operation completed successfully." />
				<UAlert icon="i-heroicons-exclamation-triangle" color="yellow" variant="soft" title="Warning Alert" description="Please review this warning message." />
				<UAlert icon="i-heroicons-x-circle" color="red" variant="soft" title="Error Alert" description="An error occurred. Please try again." />
			</div>
		</UPageSection>

		<!-- Badges Section -->
		<UPageSection id="badges" title="Badges" class="mt-12">
			<div class="space-y-4">
				<div>
					<h3 class="text-lg font-semibold mb-4">Badge Variants</h3>
					<div class="flex flex-wrap gap-2">
						<UBadge>Default</UBadge>
						<UBadge color="primary">Primary</UBadge>
						<UBadge color="gray">Gray</UBadge>
						<UBadge color="green">Green</UBadge>
						<UBadge color="yellow">Yellow</UBadge>
						<UBadge color="red">Red</UBadge>
					</div>
				</div>
				<div>
					<h3 class="text-lg font-semibold mb-4">Badge Variants</h3>
					<div class="flex flex-wrap gap-2">
						<UBadge variant="solid">Solid</UBadge>
						<UBadge variant="outline">Outline</UBadge>
						<UBadge variant="soft">Soft</UBadge>
						<UBadge variant="subtle">Subtle</UBadge>
					</div>
				</div>
			</div>
		</UPageSection>

		<!-- Navigation -->
		<!-- <UPageSection id="navigation" title="Navigation" class="mt-12">
			<div class="space-y-6">
				<div>
					<h3 class="text-lg font-semibold mb-4">Vertical Navigation</h3>
					<UVerticalNavigation :links="navLinks" />
				</div>
			</div>
		</UPageSection> -->
	</div>
</template>

<script setup>
import { html_beautify } from 'js-beautify'

const rteDisabled = ref(false)
const formData = ref({
	text: '',
	email: '',
	password: '',
	textarea: '',
	select: null,
	checkbox: false,
	radio: 'option1'
})

const richTextContent = ref('')

// Pretty print HTML for better readability (compact version)
const prettyPrintHtml = (html) => {
	if (!html) return ''

	// Compact HTML formatting with minimal indentation
	return html_beautify(html)
}

const selectOptions = [
	{ label: 'Option 1', value: 'option1' },
	{ label: 'Option 2', value: 'option2' },
	{ label: 'Option 3', value: 'option3' }
]

const radioOptions = [
	{ label: 'Option 1', value: 'option1' },
	{ label: 'Option 2', value: 'option2' },
	{ label: 'Option 3', value: 'option3' }
]

const navLinks = [
	{
		label: 'Home',
		icon: 'i-heroicons-home',
		to: '/'
	},
	{
		label: 'Design System',
		icon: 'i-heroicons-paint-brush',
		to: '/design-system'
	},
	{
		label: 'Notes',
		icon: 'i-heroicons-document-text',
		to: '/notes'
	},
	{
		label: 'Action Items',
		icon: 'i-heroicons-check-circle',
		to: '/action-items'
	},
	{
		label: 'Settings',
		icon: 'i-heroicons-cog-6-tooth',
		to: '/settings'
	}
]

useHead({
	title: 'Design System Review'
})
</script>

<style scoped>
.html-output {
	font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
	font-size: 0.75rem;
	line-height: 1.5;
	background: rgba(0, 0, 0, 0.3);
	border-radius: 0.25rem;
	padding: 0.75rem;
	margin-top: 0.5rem;
	overflow-x: auto;
	white-space: pre-wrap;
	word-break: break-word;
}

.html-output code {
	display: block;
	color: var(--ui-text);
	background: transparent;
}
</style>

<script setup>
</script>
