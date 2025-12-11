<script setup>
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
