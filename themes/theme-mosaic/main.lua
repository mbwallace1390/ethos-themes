-- Mosaic
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
        key = "Mosaic",
        name = "Mosaic",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x24, 0x38, 0x36), -- SECONDARY_BGCOLOR
            lcd.RGB(0x2F, 0xC7, 0xA8), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0C, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x73, 0x80, 0x7F), -- DISABLE_COLOR
            lcd.RGB(0x0D, 0x23, 0x20), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9B, 0xE1, 0xD5), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x06, 0x11, 0x0F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xC9, 0x4A), -- ACTIVE_COLOR
            lcd.RGB(0x93, 0x9E, 0x9E), -- INACTIVE_COLOR
            lcd.RGB(0xFE, 0xCE, 0x5C), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x40, 0x51, 0x50), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x06, 0x11, 0x0F), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-mosaic.png", "toolbar-mosaic-x18.png"),
    })
end

return { init = init }
