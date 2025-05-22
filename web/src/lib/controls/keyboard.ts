import type {State, Vector} from "./state"
import {clamp} from "../util/clamp";
import type {Source} from "./source";
import type {Action} from "svelte/action";

export class Keyboard implements Source {
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

    private _pressed: Set<string> = new Set()
    private _cameraXTimeout?: NodeJS.Timeout
    private _cameraYTimeout?: NodeJS.Timeout

    constructor() {
        window.addEventListener('keydown', (e) => this.handleKeydown(e))
        window.addEventListener('keyup', (e) => this.handleKeyup(e))
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

    private handleKeydown(e: KeyboardEvent) {
        if (this._pressed.has(e.key)) return
        this._pressed.add(e.key)
        this.handleDrive()
        this.handleSteer()
        this.handleCamera()
        this.handleBuzzer()
    }

    private handleKeyup(e: KeyboardEvent) {
        this._pressed.delete(e.key)
        this.handleDrive()
        this.handleSteer()
        this.handleCamera()
        this.handleBuzzer()
    }

    private handleDrive() {
        let drive = 0
        if (this._pressed.has("w")) {
            drive += 1
        }
        if (this._pressed.has("s")) {
            drive -= 1
        }

        if (drive !== this.state.drive) {
            this.state.drive = drive
            this.notifyDriveChange()
        }
    }

    private handleSteer() {
        let steer = 0
        if (this._pressed.has("a")) {
            steer -= 30
        }
        if (this._pressed.has("d")) {
            steer += 30
        }

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
        const handle = () => {
            let x = this.state.camera.x
            if (this._pressed.has("ArrowUp")) {
                x += 5
            }
            if (this._pressed.has("ArrowDown")) {
                x -= 5
            }
            x = clamp(x, -20, 45)

            if (x !== this.state.camera.x) {
                this.state.camera.x = x
                this.notifyCameraChange()
            }
        }

        if (this._pressed.has("ArrowUp") || this._pressed.has("ArrowDown")) {
            clearInterval(this._cameraXTimeout)
            this._cameraXTimeout = setInterval(() => handle(), 250)
            handle()
        } else if (!this._pressed.has("ArrowUp") && !this._pressed.has("ArrowDown")) {
            clearInterval(this._cameraXTimeout)
        }
    }

    private handleCameraY() {
        const handle = () => {
            let y = this.state.camera.y
            if (this._pressed.has("ArrowLeft")) {
                y -= 5
            }
            if (this._pressed.has("ArrowRight")) {
                y += 5
            }
            y = clamp(y, -45, 45)

            if (y !== this.state.camera.y) {
                this.state.camera.y = y
                this.notifyCameraChange()
            }
        }

        if (this._pressed.has("ArrowLeft") || this._pressed.has("ArrowRight")) {
            clearInterval(this._cameraYTimeout)
            this._cameraYTimeout = setInterval(() => handle(), 250)
            handle()
        } else if (!this._pressed.has("ArrowLeft") && !this._pressed.has("ArrowRight")) {
            clearInterval(this._cameraYTimeout)
        }
    }

    private handleBuzzer() {
        let buzzer = 0
        if (this._pressed.has("f")) {
            buzzer = 1
        }

        if (buzzer !== this.state.buzzer) {
            this.state.buzzer = buzzer
            this.notifyBuzzerChange()
        }
    }
}

export const keyboard = new Keyboard()
