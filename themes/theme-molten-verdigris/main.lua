-- Molten Verdigris
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
        key = "MltVerd",
        name = "Molten Verdigris",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF1, 0xEC), -- PRIMARY_COLOR
            lcd.RGB(0x21, 0x1B, 0x17), -- SECONDARY_BGCOLOR
            lcd.RGB(0x2D, 0xEB, 0xAA), -- HIGHLIGHT_COLOR
            lcd.RGB(0x10, 0x0C, 0x0A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6A, 0x67, 0x64), -- DISABLE_COLOR
            lcd.RGB(0x15, 0x11, 0x0F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9B, 0xEE, 0xCE), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x0A, 0x08, 0x07), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x9C, 0xFF, 0xE0), -- ACTIVE_COLOR
            lcd.RGB(0x86, 0x83, 0x80), -- INACTIVE_COLOR
            lcd.RGB(0xA7, 0xFD, 0xE1), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x46, 0x42, 0x40), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x38), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0A, 0x08, 0x07), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-molten-verdigris.png", "toolbar-molten-verdigris-x18.png"),
    })
end

return { init = init }
