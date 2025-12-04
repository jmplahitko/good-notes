export default defineAppConfig({
	ui: {
		input: {
			variants: {
				variant: {
					soft: 'text-highlighted bg-elevated/15 hover:bg-elevated/25 focus:bg-elevated/25 disabled:bg-elevated/50',
					outline: 'bg-input text-highlighted ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
				}
			}
		},
		textarea: {
			variants: {
				variant: {
					outline: 'bg-input text-highlighted ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
				}
			}
		},
		select: {
			variants: {
				variant: {
					outline: 'bg-input text-highlighted ring ring-inset ring-accented focus:ring-2 focus:ring-inset focus:ring-primary'
				}
			}
		}
	}
})
