-- Golden Courage
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
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
        key = "GoldCr",
        name = "Golden Courage",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x4A, 0x3E, 0x1B), -- SECONDARY_BGCOLOR
            lcd.RGB(0xF4, 0xC5, 0x42), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x8C, 0x89, 0x7D), -- DISABLE_COLOR
            lcd.RGB(0x30, 0x28, 0x12), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xF5, 0xE0, 0xA7), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x17, 0x13, 0x0A), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xF0, 0xA6), -- ACTIVE_COLOR
            lcd.RGB(0xAC, 0xAA, 0xA2), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0xF0, 0xA6), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x75, 0x61, 0x26), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x17, 0x13, 0x0A), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-golden-courage.png", "toolbar-golden-courage-x18.png"),
    })
end

return { init = init }
