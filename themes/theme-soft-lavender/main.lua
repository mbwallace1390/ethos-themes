-- Soft Lavender
-- Lightweight standalone ETHOS theme.
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
        key = "SoftLav",
        name = "Soft Lavender",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x39, 0x34, 0x45), -- SECONDARY_BGCOLOR
            lcd.RGB(0xB7, 0x9C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x1E, 0x1B, 0x29), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x80, 0x7E, 0x88), -- DISABLE_COLOR
            lcd.RGB(0x2A, 0x26, 0x33), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD6, 0xCA, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x8C, 0xE7, 0xB4), -- SAFE_COLOR
            lcd.RGB(0x1C, 0x1A, 0x24), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x75, 0x80), -- ERROR_COLOR
            lcd.RGB(0xB7, 0x9C, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x9E, 0x9E, 0xA5), -- INACTIVE_COLOR
            lcd.RGB(0xC3, 0xAE, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x61, 0x5E, 0x69), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x75), -- WARNING_COLOR
            lcd.RGB(0x14, 0x2A, 0x1E), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1C, 0x1A, 0x24), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-soft-lavender.png", "toolbar-soft-lavender-x18.png"),
    })
end

return { init = init }
