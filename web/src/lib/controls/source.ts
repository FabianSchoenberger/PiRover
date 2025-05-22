import type {Vector, State} from "./state"

export interface Source {
    state: State

    reset(): void

    onDriveChange(callback: (speed: number) => void): void

    onSteerChange(callback: (steer: number) => void): void

    onCameraChange(callback: (camera: Vector) => void): void

    onBuzzerChange(callback: (buzzer: number) => void): void
}
