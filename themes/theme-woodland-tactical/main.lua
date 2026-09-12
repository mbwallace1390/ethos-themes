-- Woodland Tactical
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
        key = "WoodTac",
        name = "Woodland Tactical",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xEE, 0xF0, 0xD8), -- PRIMARY_COLOR
            lcd.RGB(0x39, 0x43, 0x2A), -- SECONDARY_BGCOLOR
            lcd.RGB(0xB7, 0xC9, 0x6B), -- HIGHLIGHT_COLOR
            lcd.RGB(0x17, 0x1C, 0x0C), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x86, 0x8D, 0x72), -- DISABLE_COLOR
            lcd.RGB(0x27, 0x2F, 0x1D), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xCB, 0xD2, 0xA4), -- SECONDARY_COLOR
            lcd.RGB(0x7F, 0xE0, 0x7B), -- SAFE_COLOR
            lcd.RGB(0x16, 0x1C, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5B, 0x4F), -- ERROR_COLOR
            lcd.RGB(0xE9, 0xA4, 0x41), -- ACTIVE_COLOR
            lcd.RGB(0xA7, 0xAE, 0x90), -- INACTIVE_COLOR
            lcd.RGB(0xE9, 0xA4, 0x41), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x58, 0x63, 0x42), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xF5, 0xC6, 0x5D), -- WARNING_COLOR
            lcd.RGB(0x0A, 0x18, 0x08), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x16, 0x1C, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-woodland-tactical.png", "toolbar-woodland-tactical-x18.png"),
    })
end

return { init = init }
