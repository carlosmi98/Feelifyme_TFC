import { useDocumentTitle } from "../../../../hooks/useDocumentTitle"
import { ReSumenCronologico } from "./components/ReSumenCronologico"


export const ResumenDiarioCronológico = () => {
    useDocumentTitle('Resumen Diario');
    return (
        <ReSumenCronologico />
    )
}

