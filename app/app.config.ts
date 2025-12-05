export default defineAppConfig({
	ui: {
		container: {
			base: 'w-full max-w-(--ui-container) mx-auto px-4 py-8'
		},
		input: {
			slots: {
				root: 'w-full',
			},
			variants: {
				variant: {
					soft: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default',
					subtle: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default ring-default',
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
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
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
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
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
				}
			}
		}
	}
})
