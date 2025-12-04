export default defineAppConfig({
	ui: {
		input: {
			variants: {
				variant: {
					soft: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default',
					subtle: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default ring-default',
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
				}
			}
		},
		textarea: {
			variants: {
				variant: {
					soft: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default',
					subtle: 'text-default bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-default ring-default',
					outline: 'bg-input text-default ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
				}
			}
		},
		select: {
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
