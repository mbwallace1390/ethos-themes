# Aviation HUD X18 compatibility test

This beta package tests automatic toolbar selection between standard 480px X18 radios and 800px X20-class radios.

- Test ZIP: `Aviation-HUD-X18-Test-v1.0.1-beta1.zip`
- X18 toolbar: 464x50
- X20 toolbar: 784x50
- Selection source: `system.getVersion().lcdWidth`
- Rotorflight and RF Suite files are not modified

Replace the existing `theme-aviation-hud` folder, restart ETHOS, and select **Aviation HUD**. Confirm that the toolbar fills the available width without cropping, squeezing, blank space, or misplaced artwork.
