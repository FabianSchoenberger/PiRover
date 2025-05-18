<script lang="ts">

    interface Props {
        ws: WebSocket | undefined
    }

    let {
        ws
    }: Props = $props()

    let src = $state("");

    $effect(() => {
        if (!ws) return;

        ws.addEventListener("message", function ({data}) {
            src = `data:image/jpeg;base64,${data}`;
        });
    })
</script>

{#if src}
    <img {src}/>
{/if}
