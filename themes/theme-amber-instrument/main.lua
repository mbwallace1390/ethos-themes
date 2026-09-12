-- Amber Instrument
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
        key = "Amber",
        name = "Amber Instrument",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF9, 0xDC, 0x9B), -- PRIMARY_COLOR
            lcd.RGB(0x2E, 0x28, 0x1A), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0xB0, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0x14, 0x11, 0x09), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x73, 0x71, 0x6C), -- DISABLE_COLOR
            lcd.RGB(0x1F, 0x1A, 0x10), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xD5, 0x82), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x11, 0x0E, 0x08), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xB0, 0x00), -- ACTIVE_COLOR
            lcd.RGB(0x91, 0x8F, 0x8B), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0xB0, 0x00), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x4D, 0x46), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x11, 0x0E, 0x08), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-amber-instrument.png", "toolbar-amber-instrument-x18.png"),
    })
end

return { init = init }
