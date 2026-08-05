# Application Launch

## Import Module

``` js
import launch from '@system.launch'
```

## Interface Definitions

### `launch` <decl type="(app: string): Promise<bool>" method/>

Launches the specified application and brings it to the foreground. `app` is a string representing the ID of an installed application. The returned Promise indicates whether the application was loaded successfully.

### `inactive` <decl type="(app?: string): Promise<void>" method/>

Switches the application to the background. `app` is the ID of a launched application. If no parameter is specified, the current application is switched to the background. Only foreground applications can be switched to the background.

### `exit` <decl type="(app?: string): Promise<void>" method />

Exits an application. The `app` parameter is the ID of a launched application. If no parameter is specified, the current application will be exited.

### `getRunning` <decl type="(): string[]" method />

Gets the list of running application package names, including those in the background.