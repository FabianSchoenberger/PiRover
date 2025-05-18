<script lang="ts">
    import Camera from "./lib/Camera.svelte";
    import Controls from "./lib/Controls.svelte";

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
    <div class="flex">
        <img src="../logo.png" class="logo"/>
        <div class="connect-form">
            <input type="text" bind:value={ip} class="ip-input" placeholder="Enter IP Address"/>
            <button onclick={connect} class="connect-button">Connect</button>
        </div>
        <Controls {enabled}
                  onDriveChange={handleDriveChange}
                  onSteerChange={handleSteerChange}
                  onCameraChange={handleCameraChange}
        />
        <div class="slider-container">
            <label for="speed">Speed Multiplier:</label>
            <input
                    type="range"
                    id="speed"
                    min="0"
                    max="1"
                    step="0.01"
                    bind:value={speedMult}
            />
            <span class="value">{speedMult.toFixed(2)}</span>
        </div>
    </div>
    <div class="camera">
        <Camera {ws}/>
    </div>
</main>

<style>
    :root {
        --primary-color: #D28F2E;
        --primary-color-dark: #b37d26;
    }
    .camera {
        margin: auto;
    }
    .logo {
        width: 150px;
        height: 150px;
    }
    .flex {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-bottom: 20px;
    }

    @media (max-width: 1200px) {
        .flex {
            flex-direction: column;
            gap: 20px;
            align-items: center;
        }
    }
    .connect-form {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: sans-serif;
    }
    .ip-input {
        padding: 10px 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 1em;
        outline: none;
        transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    .ip-input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 0.2rem rgba(210, 143, 46, 0.25);
    }
    .connect-button {
        padding: 10px 20px;
        background-color: var(--primary-color);
        color: #fff;
        border: none;
        border-radius: 4px;
        font-size: 1em;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
    }
    .connect-button:hover {
        background-color: var(--primary-color-dark);
    }
    .connect-button:active {
        background-color: var(--primary-color-dark);
    }
    .connect-button:focus {
        outline: none;
        box-shadow: 0 0 0 0.2rem rgba(210, 143, 46, 0.25);
    }
    .slider-container {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: sans-serif;
    }

    input[type="range"] {
        width: 200px;
        accent-color: var(--primary-color);
    }

    .value {
        font-size: 1em;
        color: var(--primary-color);
        width: 40px;
        text-align: right;
    }
</style>
