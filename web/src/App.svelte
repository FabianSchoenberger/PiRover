<script lang="ts">
    import Camera from "./lib/Camera.svelte";
    import Controls from "./lib/Controls.svelte";
    import type {Vector} from "./lib/controls/state";

    let speedMult = $state(1);

    let ip = $state("10.173.8.45")
    let ws: WebSocket | undefined = $state()
    let enabled = $derived(ws !== undefined)

    function connect() {
        ws = new WebSocket(`ws://${ip}:80`);
    }

    function handleDriveChange(drive: number) {
        console.log("speed", drive)
        ws.send(JSON.stringify({
            type: "drive",
            speed: drive * speedMult
        }))
    }

    function handleSteerChange(steer: number) {
        console.log("steer", steer)
        ws.send(JSON.stringify({
            type: "steer",
            angle: steer
        }))
    }

    function handleCameraChange({x, y}: Vector) {
        console.log("camera", x, y)
        ws.send(JSON.stringify({
            type: "camera",
            x,
            y
        }))
    }

    function handleBuzzerChange(buzzer: number) {
        console.log("buzzer", buzzer)
        ws.send(JSON.stringify({
            type: "buzzer",
            buzzer
        }))
    }

    let led = $state("off");
    $effect(() => {
        console.log(led, ws)
        if (ws === undefined) return;
        if (led == "off") handleLed({r: 0, g: 0, b: 0});
        else if (led == "red") handleLed({r: 1, g: 0, b: 0});
        else if (led == "yellow") handleLed({r: 1, g: 1, b: 0});
    })
    function handleLed({r, g, b}: {r: number, g: number, b: number}) {
        console.log("led", r, g, b)
        ws.send(JSON.stringify({
            type: "led",
            red: r,
            green: g,
            blue: b
        }))
    }
</script>

<main>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 items-center content-center justify-center justify-items-center gap-4">
        <img src="../logo.png" class="size-40" alt="logo"/>
        <div class="flex items-center gap-2">
            <input type="text" bind:value={ip} class="input-primary" placeholder="Enter IP Address"/>
            <button onclick={connect} class="button-primary">Connect</button>
        </div>
        {#if enabled}
        <Controls {enabled}
                  onDriveChange={handleDriveChange}
                  onSteerChange={handleSteerChange}
                  onCameraChange={handleCameraChange}
                  onBuzzerChange={handleBuzzerChange}
        />
        <div class="flex items-center gap-2">
            <label class="text-primary" for="speed">Speed Multiplier:</label>
            <input type="range" id="speed" min="0.1" max="1" step="0.01" bind:value={speedMult} class="accent-primary"/>
            <span class="text-primary">{speedMult.toFixed(2)}</span>
        </div>
        <div class="flex items-center gap-2">
            <button class={led === "red" ? "button-danger" : "button-grey"} onclick={() => {led === "red" ? led = "off" : led = "red"}}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                </svg>
                Red
            </button>
            <button class={led === "yellow" ? "button-primary" : "button-grey"} onclick={() => {led === "yellow" ? led = "off" : led = "yellow"}}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                </svg>
                Yellow
            </button>
        </div>
        {/if}
    </div>
    {#if enabled}
    <div class="flex justify-center">
        <Camera {ws}/>
    </div>
    {/if}
</main>

