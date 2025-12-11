<script setup lang="ts">
// SEO and app configuration
useHead({
	meta: [
		{ name: 'viewport', content: 'width=device-width, initial-scale=1' }
	],
	link: [
		{ rel: 'icon', href: '/favicon.ico' }
	],
	htmlAttrs: {
		lang: 'en',
		class: 'dark'
	}
})

const colorMode = useColorMode()
colorMode.preference = 'dark'
colorMode.value = 'dark'

const title = 'Good Notes'
const description = 'A desktop note-taking application'

useSeoMeta({
	title,
	description,
	ogTitle: title,
	ogDescription: description,
	twitterCard: 'summary_large_image'
})

// Components
import CreateActionItemModal from './components/CreateActionItemModal.vue'

// Global navigation
const router = useRouter()

// Global hotkey handler for Cmd+N (Mac) or Ctrl+N (Windows/Linux)
const handleGlobalKeydown = (event: KeyboardEvent) => {
	if ((event.metaKey || event.ctrlKey) && event.key === '.') {
		event.preventDefault() // Prevent default browser behavior
		router.push('/notes/create')
	}
}

// Add global keyboard event listener
onMounted(() => {
	document.addEventListener('keydown', handleGlobalKeydown)
})

onUnmounted(() => {
	document.removeEventListener('keydown', handleGlobalKeydown)
})

</script>

<template>
	<UApp>
		<UHeader title="Good Notes">
			<template #right>
				<CreateActionItemModal />
				<UButton to="/design-system" icon="i-heroicons-paint-brush" aria-label="Design System" color="neutral" variant="ghost" />
			</template>
		</UHeader>

		<UMain>
			<NuxtPage />
		</UMain>
	</UApp>
</template>
