import type {State} from "./state"

export interface Source {
    state: State

    reset(): void
    onDriveChange(callback: (speed: number) => void): void
    onSteerChange(callback: (steer: number) => void): void
    onCameraChange(callback: (camera: {x: number, y: number}) => void): void
}
