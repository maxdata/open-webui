<script lang="ts">
	import { run } from 'svelte/legacy';

	import { createEventDispatcher, onMount } from 'svelte';
	import { toast } from 'svelte-sonner';

	const dispatch = createEventDispatcher();

	import { knowledge, prompts } from '$lib/stores';

	import { removeLastWordFromString } from '$lib/utils';
	import { getPrompts } from '$lib/apis/prompts';
	import { getKnowledgeBases } from '$lib/apis/knowledge';

	import Prompts from './Commands/Prompts.svelte';
	import Knowledge from './Commands/Knowledge.svelte';
	import Models from './Commands/Models.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';

	interface Props {
		prompt?: string;
		files?: any;
	}

	let { prompt = $bindable(''), files = $bindable([]) }: Props = $props();

	let loading = $state(false);
	let commandElement = $state(null);

	export const selectUp = () => {
		commandElement?.selectUp();
	};

	export const selectDown = () => {
		commandElement?.selectDown();
	};

	let command = $state('');

	let show = $state(false);


	const init = async () => {
		loading = true;
		await Promise.all([
			(async () => {
				prompts.set(await getPrompts(localStorage.token));
			})(),
			(async () => {
				knowledge.set(await getKnowledgeBases(localStorage.token));
			})()
		]);
		loading = false;
	};
	run(() => {
		command = prompt?.split('\n').pop()?.split(' ')?.pop() ?? '';
	});
	run(() => {
		show = ['/', '#', '@'].includes(command?.charAt(0)) || '\\#' === command.slice(0, 2);
	});
	run(() => {
		if (show) {
			init();
		}
	});
</script>

{#if show}
	{#if !loading}
		{#if command?.charAt(0) === '/'}
			<Prompts bind:this={commandElement} bind:prompt bind:files {command} />
		{:else if (command?.charAt(0) === '#' && command.startsWith('#') && !command.includes('# ')) || ('\\#' === command.slice(0, 2) && command.startsWith('#') && !command.includes('# '))}
			<Knowledge
				bind:this={commandElement}
				bind:prompt
				command={command.includes('\\#') ? command.slice(2) : command}
				on:youtube={(e) => {
					console.log(e);
					dispatch('upload', {
						type: 'youtube',
						data: e.detail
					});
				}}
				on:url={(e) => {
					console.log(e);
					dispatch('upload', {
						type: 'web',
						data: e.detail
					});
				}}
				on:select={(e) => {
					console.log(e);
					files = [
						...files,
						{
							...e.detail,
							status: 'processed'
						}
					];

					dispatch('select');
				}}
			/>
		{:else if command?.charAt(0) === '@'}
			<Models
				bind:this={commandElement}
				{command}
				on:select={(e) => {
					prompt = removeLastWordFromString(prompt, command);

					dispatch('select', {
						type: 'model',
						data: e.detail
					});
				}}
			/>
		{/if}
	{:else}
		<div
			id="commands-container"
			class="pl-3 pr-14 mb-3 text-left w-full absolute bottom-0 left-0 right-0 z-10"
		>
			<div class="flex w-full rounded-xl border border-gray-50 dark:border-gray-850">
				<div
					class="max-h-60 flex flex-col w-full rounded-xl bg-white dark:bg-gray-900 dark:text-gray-100"
				>
					<Spinner />
				</div>
			</div>
		</div>
	{/if}
{/if}
