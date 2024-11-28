<script lang="ts">
	import { run } from 'svelte/legacy';

	interface Props {
		token: any;
		onClick?: Function;
	}

	let { token, onClick = () => {} }: Props = $props();

	let id = $state('');
	function extractDataAttribute(input) {
		// Use a regular expression to extract the value of the `data` attribute
		const match = input.match(/data="([^"]*)"/);
		// Check if a match was found and return the first captured group
		return match ? match[1] : null;
	}

	run(() => {
		id = extractDataAttribute(token.text);
	});
</script>

<button
	class="text-xs font-medium w-fit translate-y-[2px] px-2 py-0.5 dark:bg-white/5 dark:text-white/60 dark:hover:text-white bg-gray-50 text-black/60 hover:text-black transition rounded-lg"
	onclick={() => {
		onClick(id);
	}}
>
	<span class="line-clamp-1">
		{id}
	</span>
</button>
