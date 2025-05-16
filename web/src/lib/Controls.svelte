<script lang="ts">
    import {keyboard} from "./controls/keyboard";
    import {gamepad} from "./controls/gamepad";

    interface Props {
        enabled: boolean
        onDriveChange: Action<number>
        onSteerChange: Action<number>
        onCameraChange: Action<Vector>
    }

    const {
        enabled,
        onDriveChange,
        onSteerChange,
        onCameraChange
    }: Props = $props()

    let source = $state(keyboard);

    $effect(() => {
        source.reset()
        if (enabled) {
            source.onDriveChange(onDriveChange)
            source.onSteerChange(onSteerChange)
            source.onCameraChange(onCameraChange)
        }
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

<button onclick={toggleSource}>
    {source === keyboard ? "keyboard" : "gamepad"}
</button>
