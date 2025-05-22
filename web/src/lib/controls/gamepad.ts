import type {State, Vector} from "./state"
import type {Source} from "./source";
import {scale} from "../util/scale";
import type {Action} from "svelte/action";

// gamepad buttons
// 0 = A
// 1 = B
// 2 = Y
// 3 = X
// 6 = Left Trigger
// 7 = Right Trigger
// 10 = Left Stick
// 11 = Right Stick

const X = 3

export class Gamepad implements Source {
    public state: State = {
        drive: 0,
        steer: 0,
        camera: {
            x: 0,
            y: 0
        },
        buzzer: 0
    };

    private _driveChange?: Action<number>
    private _steerChange?: Action<number>
    private _cameraChange?: Action<Vector>
    private _buzzerChange?: Action<number>

    private _buttons: Set<string> = new Set()
    private _leftStick!: Vector
    private _rightStick!: Vector
    private _triggers!: { left: number, right: number }
    private _timeout?: NodeJS.Timeout

    constructor() {
        window.addEventListener("gamepadconnected", (e) => this.handleConnected())
        window.addEventListener("gamepaddisconnected", (e) => this.handleDisconnected())
    }

    reset() {
        this.state = {
            drive: 0,
            steer: 0,
            camera: {
                x: 0,
                y: 0
            },
            buzzer: 0
        }
        this._driveChange = undefined
        this._steerChange = undefined
        this._cameraChange = undefined
        this._buzzerChange = undefined
    }

    onDriveChange(callback: Action<number>) {
        this._driveChange = callback
    }

    onSteerChange(callback: Action<number>) {
        this._steerChange = callback
    }

    onCameraChange(callback: Action<Vector>) {
        this._cameraChange = callback
    }

    onBuzzerChange(callback: Action<number>) {
        this._buzzerChange = callback
    }

    private notifyDriveChange() {
        this._driveChange?.(this.state.drive)
    }

    private notifySteerChange() {
        this._steerChange?.(this.state.steer)
    }

    private notifyCameraChange() {
        this._cameraChange?.(this.state.camera)
    }

    private notifyBuzzerChange() {
        this._buzzerChange?.(this.state.buzzer)
    }

    private handleConnected() {
        clearInterval(this._timeout)
        setInterval(() => {
            const gamepads = navigator.getGamepads();
            if (!gamepads) {
                return;
            }

            const gp = gamepads[0]!;
            const buttons = gp.buttons;
            this._buttons.clear()
            for (let i = 0; i < buttons.length; i++) {
                const button = gp.buttons[i]
                if (i == X && button.pressed) {
                    this._buttons.add("X")
                }
            }
            const axes = gp.axes
            this._leftStick = {x: axes[0], y: axes[1]}
            this._rightStick = {x: axes[2], y: axes[3]}
            this._triggers = {left: axes[5], right: axes[4]}
            if (this._triggers.left === 0) {
                this._triggers.left = -1
            }
            if (this._triggers.right === 0) {
                this._triggers.right = -1
            }

            this.handleDrive()
            this.handleSteer()
            this.handleCamera()
            this.handleBuzzer()
        }, 100)
    }

    private handleDisconnected() {
        clearInterval(this._timeout)
    }

    private handleDrive() {
        let drive = 0
        drive -= scale(this._triggers.left, -1, 1, 0, 1)
        drive += scale(this._triggers.right, -1, 1, 0, 1)

        if (drive !== this.state.drive) {
            this.state.drive = drive
            this.notifyDriveChange()
        }
    }

    private handleSteer() {
        let steer = scale(this._leftStick.x, -1, 1, -30, 30)

        if (steer !== this.state.steer) {
            this.state.steer = steer
            this.notifySteerChange()
        }
    }

    private handleCamera() {
        this.handleCameraX()
        this.handleCameraY()
    }

    private handleCameraX() {
        let x = scale(-this._rightStick.y, -1, 1, -20, 45)

        if (x !== this.state.camera.x) {
            this.state.camera.x = x
            this.notifyCameraChange()
        }
    }

    private handleCameraY() {
        let y = scale(this._rightStick.x, -1, 1, -45, 45)

        if (y !== this.state.camera.y) {
            this.state.camera.y = y
            this.notifyCameraChange()
        }
    }

    private handleBuzzer() {
        let buzzer = 0
        if (this._buttons.has("X")) {
            buzzer = 1
        }

        if (buzzer !== this.state.buzzer) {
            this.state.buzzer = buzzer
            this.notifyBuzzerChange()
        }
    }
}

export const gamepad = new Gamepad()
