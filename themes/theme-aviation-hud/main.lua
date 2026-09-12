-- Aviation HUD
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and type(version.lcdWidth) == "number" and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function loadToolbar(largeFile, smallFile)
    -- Optional artwork must not prevent registration when it cannot be loaded.
    local ok, bitmap = pcall(lcd.loadBitmap, selectToolbar(largeFile, smallFile))
    if ok and bitmap then
        return bitmap
    end
    return nil
end

local function init()
    -- Skip unsupported firmware before creating colors or loading artwork.
    if type(system.registerTheme) ~= "function" then return end
    system.registerTheme({
        key = "AvHUD",
        name = "Aviation HUD",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xD9, 0xFF, 0xE2), -- PRIMARY_COLOR
            lcd.RGB(0x12, 0x27, 0x1A), -- SECONDARY_BGCOLOR
            lcd.RGB(0x62, 0xFF, 0x86), -- HIGHLIGHT_COLOR
            lcd.RGB(0x06, 0x14, 0x0A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x56, 0x73, 0x5D), -- DISABLE_COLOR
            lcd.RGB(0x0B, 0x1B, 0x11), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9A, 0xEF, 0xAC), -- SECONDARY_COLOR
            lcd.RGB(0x62, 0xFF, 0x86), -- SAFE_COLOR
            lcd.RGB(0x05, 0x0D, 0x08), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4B, 0x4B), -- ERROR_COLOR
            lcd.RGB(0xB8, 0xFF, 0x4A), -- ACTIVE_COLOR
            lcd.RGB(0x70, 0x91, 0x78), -- INACTIVE_COLOR
            lcd.RGB(0xB8, 0xFF, 0x4A), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x29, 0x4E, 0x33), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD2, 0x4A), -- WARNING_COLOR
            lcd.RGB(0x03, 0x10, 0x06), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x05, 0x0D, 0x08), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-aviation-hud.png", "toolbar-aviation-hud-x18.png"),
    })
end

return { init = init }
