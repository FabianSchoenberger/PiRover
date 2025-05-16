<script lang="ts">
    import {ws} from "./websocket";

    let src = $state("");

    ws.addEventListener("message", function ({data}) {
        src = `data:image/jpeg;base64,${data}`;
    });
</script>

{#if src}
    <img {src}/>
{/if}
