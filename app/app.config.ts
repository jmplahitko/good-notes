export default defineAppConfig({
	ui: {
		container: {
			base: 'w-full max-w-(--ui-container) mx-auto px-4 py-8'
		},
		header: {
			slots: {
				container: 'w-full max-w-(--ui-container) mx-auto p-0',
				title: 'text-md text-defaultfont-bold',
			}
		},
		input: {
			slots: {
				root: 'w-full',
			},
			variants: {
				variant: {
					soft: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default',
					subtle: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default ring-default',
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary',
					ghost: 'bg-transparent text-default hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default'
				}
			}
		},
		textarea: {
			slots: {
				root: 'w-full',
			},
			variants: {
				variant: {
					soft: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default',
					subtle: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default ring-default',
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary',
					ghost: 'bg-transparent text-default hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default'
				}
			}
		},
		select: {
			slots: {
				base: 'w-full',
			},
			variants: {
				variant: {
					soft: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default',
					subtle: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default ring-default',
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary',
					ghost: 'bg-transparent text-default hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default'
				}
			}
		}
	}
})
