-- Soft Coral
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
        key = "SCoral",
        name = "Soft Coral",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x45, 0x36, 0x34), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x9A, 0x8B), -- HIGHLIGHT_COLOR
            lcd.RGB(0x29, 0x1C, 0x1B), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x87, 0x82, 0x82), -- DISABLE_COLOR
            lcd.RGB(0x33, 0x28, 0x26), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xC8, 0xC2), -- SECONDARY_COLOR
            lcd.RGB(0x8C, 0xE7, 0xB4), -- SAFE_COLOR
            lcd.RGB(0x24, 0x1B, 0x1A), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x75, 0x80), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x9A, 0x8B), -- ACTIVE_COLOR
            lcd.RGB(0xA5, 0xA2, 0xA2), -- INACTIVE_COLOR
            lcd.RGB(0xFD, 0xAD, 0xA1), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x67, 0x60, 0x5F), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x75), -- WARNING_COLOR
            lcd.RGB(0x14, 0x2A, 0x1E), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x24, 0x1B, 0x1A), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-soft-coral.png", "toolbar-soft-coral-x18.png"),
    })
end

return { init = init }
