export default defineAppConfig({
	ui: {
		input: {
			slots: {
				base: [
					'w-full rounded-sm border-0 appearance-none placeholder:text-dimmed focus:outline-none disabled:cursor-not-allowed disabled:opacity-75',
					'transition-colors'
				],
			},
			variants: {
				variant: {
					outline: 'text-highlighted bg-input ring ring-inset ring-accented focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-primary'
				}
			}
		},
		textarea: {
			variants: {
				variant: {
					outline: 'text-highlighted bg-input ring ring-inset ring-accented focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-primary'
				}
			}
		},
		select: {
			variants: {
				variant: {
					outline: 'text-highlighted bg-input ring ring-inset ring-accented focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-primary'
				}
			}
		}
	}
})
