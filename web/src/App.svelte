<script lang="ts">
    import Camera from "./lib/Camera.svelte";
    import Controls from "./lib/Controls.svelte";

    const speedMult = 1

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

    function handleCameraChange({x, y}: number) {
        console.log("camera", x, y)
        ws.send(JSON.stringify({
            type: "camera",
            x,
            y
        }))
    }
</script>

<main>
    <div>
        <input bind:value={ip}/>
        <button onclick={connect}>connect</button>
    </div>
    <div>
        <Controls {enabled}
                  onDriveChange={handleDriveChange}
                  onSteerChange={handleSteerChange}
                  onCameraChange={handleCameraChange}
        />
    </div>
    <div>
        <Camera {ws}/>
    </div>
</main>

<style>
</style>
