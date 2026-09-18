-- Ink & Halo
-- Ink-black panels and a quiet halo. Native ETHOS radio theme; no background tasks.
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
    -- Replace the default ETHOS logo so it cannot cover the header text.
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-transparent.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "INKHALO",
        name = "Ink & Halo",
        roundButtons = true,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFC), -- PRIMARY_COLOR
            lcd.RGB(0x17, 0x1D, 0x28), -- SECONDARY_BGCOLOR
            lcd.RGB(0xBD, 0xD7, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x08, 0x0B, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x74, 0x7F, 0x91), -- DISABLE_COLOR
            lcd.RGB(0x0D, 0x10, 0x17), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xB5, 0xBF, 0xCE), -- SECONDARY_COLOR
            lcd.RGB(0x8D, 0xC9, 0xA4), -- SAFE_COLOR
            lcd.RGB(0x08, 0x0B, 0x10), -- PAGE_BGCOLOR
            lcd.RGB(0xF2, 0x93, 0x9C), -- ERROR_COLOR
            lcd.RGB(0xBD, 0xD7, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x98, 0xA3, 0xB5), -- INACTIVE_COLOR
            lcd.RGB(0xBD, 0xD7, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x54, 0x64, 0x7A), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xE6, 0xC7, 0x86), -- WARNING_COLOR
            lcd.RGB(0x08, 0x0B, 0x10), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0D, 0x10, 0x17), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-ink-halo.png", "toolbar-ink-halo-x18.png"),
    })
end

return { init = init }
