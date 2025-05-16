<script lang="ts">
    import Camera from "./lib/Camera.svelte";
    import {ws} from "./lib/websocket";
    import {gamepad} from "./lib/controls/gamepad";
    import {keyboard} from "./lib/controls/keyboard";

    let source = $state(keyboard);

    $effect(() => {
        source.onDriveChange((drive: number) => {
            console.log("speed", drive)
            ws.send(JSON.stringify({
                type: "drive",
                speed: drive * 0.5
            }))
        })
        source.onSteerChange((steer: number) => {
            console.log("steer", steer)
            ws.send(JSON.stringify({
                type: "steer",
                angle: steer
            }))
        })
        source.onCameraChange((camera: { x: number, y: number }) => {
            console.log("camera", camera)
            ws.send(JSON.stringify({
                type: "camera",
                x: camera.x,
                y: camera.y
            }))
        })
    })

    function toggleSource() {
        source.reset()
        if (source === keyboard) {
            source = gamepad
        } else {
            source = keyboard
        }
    }
</script>

<main>
    <div>
        <button onclick={toggleSource}>source: {source === keyboard ? "keyboard" : "gamepad"}</button>
    </div>
    <div>
        <Camera/>
    </div>
</main>

<style>
</style>
