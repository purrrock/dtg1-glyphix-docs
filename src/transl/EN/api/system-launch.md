# Application jump

## Import module

``` js
import launch from '@system.launch'
```

## Interface definition

### `launch` <decl type="(app: string): Promise<bool>" method/>

Start the specified application and switch to the foreground. `app` is an installed application ID string. The returned Promise indicates whether the application is loaded successfully.

### `inactive` <decl type="(app?: string): Promise<void>" method/>

Switch the app to the background. `app` is the ID of a started application. If no parameters are specified, the current application will be switched to the background. Only foreground applications can be switched to the background.

### `exit` <decl type="(app?: string): Promise<void>" method />

Quit an application. The parameter `app` is the ID of a started application. If no parameter is specified, the current application will be exited.

### `getRunning` <decl type="(): string[]" method />

Get a list of running application package names, including those in the background.
